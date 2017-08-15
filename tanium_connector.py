# --
# File: tanium_connector.py
#
# Copyright (c) Phantom Cyber Corporation, 2014-2017
#
# This unpublished material is proprietary to Phantom Cyber.
# All rights reserved. The methods and
# techniques described herein are considered trade secrets
# and/or confidential. Reproduction or distribution, in whole
# or in part, is forbidden except by express written permission
# of Phantom Cyber Corporation.
#
# --

# Phantom imports
import phantom.app as phantom
from phantom.base_connector import BaseConnector
from phantom.action_result import ActionResult
# import phantom.utils as ph_utils

# THIS Connector imports
from tanium_consts import *

from pytanlib import pytan
import os
import json


class TaniumConnector(BaseConnector):

    # The actions supported by this connector
    ACTION_ID_LIST_SAVED_QUESTIONS = "list_saved_questions"
    ACTION_ID_EXECUTE_SAVED_QUESTION = "execute_question"
    ACTION_ID_REBOOT_SYSTEM = "reboot_system"
    ACTION_ID_TERM_PROCESS = "terminate_process"
    ACTION_ID_LIST_PROCESSES = "list_processes"
    ACTION_ID_EXECUTE_CUSTOM_QUESTION = "get_parsed_questions"
    ACTION_ID_EXECUTE_ACTION = "execute_action"
    call_index = 0

    def __init__(self):

        # Call the BaseConnectors init first
        super(TaniumConnector, self).__init__()

        self._base_url = None
        self._headers = None

    def initialize(self):

        config = self.get_config()

        # Base URL
        self._base_url = 'https://' + config[phantom.APP_JSON_DEVICE] + '/soap'

        self._headers = {'Content-type': 'text/xml; charset=\"UTF-8\"', 'SOAPAction': '\"\"'}

        verify_cert = config[phantom.APP_JSON_VERIFY]

        if (not verify_cert):
            if ('REQUESTS_CA_BUNDLE' in os.environ):
                del os.environ['REQUESTS_CA_BUNDLE']

        return phantom.APP_SUCCESS

    def _create_handler(self, result_obj):

        self.save_progress("Creating Tanium handler")

        config = self.get_config()

        # create a dictionary of arguments for the pytan handler
        handler_args = {}

        # establish our connection info for the Tanium Server
        handler_args['username'] = config[phantom.APP_JSON_USERNAME]
        handler_args['password'] = config[phantom.APP_JSON_PASSWORD]
        handler_args['host'] = config[phantom.APP_JSON_DEVICE]
        handler_args['port'] = config.get(phantom.APP_JSON_PORT, '443')  # optional

        # optional, level 0 is no output except warnings/errors
        # level 1 through 12 are more and more verbose
        handler_args['loglevel'] = 0

        # optional, use a debug format for the logging output (uses two lines per log entry)
        handler_args['debugformat'] = False

        # optional, this saves all response objects to handler.session.ALL_REQUESTS_RESPONSES
        # very useful for capturing the full exchange of XML requests and responses
        handler_args['record_all_requests'] = False

        # instantiate a handler using all of the arguments in the handler_args dictionary
        try:
            handler = pytan.Handler(**handler_args)
        except Exception as e:
            return (result_obj.set_status(phantom.APP_ERROR, "{0}".format(e.message)), None)

        version = handler.session.get_server_version()
        self.save_progress("Got Tanium version '{0}'".format(version))
        if version in handler.session.BAD_SERVER_VERSIONS:
            self.save_progress("Could not determine Tanium version. Forcing 7.0")
            handler.session.force_server_version = '7.0'

        return (phantom.APP_SUCCESS, handler)

    def _list_saved_questions(self, param):

        action_result = self.add_action_result(ActionResult(param))

        ret_val, handler = self._create_handler(action_result)

        if (phantom.is_fail(ret_val)):
            return action_result.get_status()

        # setup the arguments for the handler() class
        kwargs = {}
        kwargs["objtype"] = u'saved_question'

        self.save_progress("Querying question list on Tanium")

        try:
            response = handler.get_all(**kwargs)
        except Exception as e:
            return action_result.set_status(phantom.APP_ERROR, "Error while getting saved questions", e)

        # call the export_obj() method to convert response to JSON and store it in out
        export_kwargs = {}
        export_kwargs['obj'] = response
        export_kwargs['export_format'] = 'json'

        self.save_progress("Processing response")

        try:
            saved_questions = handler.export_obj(**export_kwargs)
        except Exception as e:
            return action_result.set_status(phantom.APP_ERROR, "Unable to parse the response as JSON", e)

        try:
            saved_questions = json.loads(saved_questions)
            saved_questions = saved_questions['saved_question']
        except Exception as e:
            return action_result.set_status(phantom.APP_ERROR, "Unable to parse the response JSON string", e)

        action_result.set_summary({TANIUM_JSON_TOTAL_SAVED_QUESTS: len(saved_questions)})

        wanted_list = ['id', 'name', 'query_text']

        for question in saved_questions:
            saved_question = {x: question[x] for x in wanted_list}
            action_result.add_data(saved_question)

        return action_result.set_status(phantom.APP_SUCCESS)

    def _question_progress(self, **kwargs):

        self.debug_print("In Progress callback")

        self.save_progress("Got progress called")

        return True

    def _cleanse_list(self, input_list):

        return ['' if x is None else x for x in input_list]

    def _ask_saved_question(self, param):
        if (param.get(TANIUM_JSON_PARSED_FLAG, TANIUM_PARSED_FLAG_DEF_VALUE)):
            self._ask_parsed_question(param)
        else:
            action_result = self.add_action_result(ActionResult(param))

            ret_val, handler = self._create_handler(action_result)

            if (phantom.is_fail(ret_val)):
                return action_result.get_status()

            # setup the arguments for the handler() class
            ques_name = param[TANIUM_JSON_QUESTION]

            kwargs = {}
            kwargs["refresh_data"] = True
            kwargs["qtype"] = u'saved'
            kwargs["name"] = ques_name
            kwargs["callback"] = {'ProgressChanged': self._question_progress}

            self.save_progress("Querying Tanium")

            try:
                response = handler.ask(**kwargs)
            except Exception as e:
                return action_result.set_status(phantom.APP_ERROR, "Error while getting saved questions", e)

            results = response.get('question_results')

            if (not response):
                return action_result.set_status(phantom.APP_ERROR, "Query did not return any results")

            # call the export_obj() method to convert response to JSON and store it in out
            export_kwargs = {}
            export_kwargs['obj'] = results
            export_kwargs['export_format'] = 'json'

            self.save_progress("Processing response")

            try:
                result_infos = handler.export_obj(**export_kwargs)
            except Exception as e:
                return action_result.set_status(phantom.APP_ERROR, "Unable to parse the response as JSON", e)

            self.debug_print("result_infos", result_infos)

            try:
                result_infos = json.loads(result_infos)
            except Exception as e:
                return action_result.set_status(phantom.APP_ERROR, "Unable to parse the response info as JSON", e)

            # columns is a list
            columns = []

            # rows is a list of rows, where each row is a list of column values
            rows = []

            for i, curr_info in enumerate(result_infos):

                curr_row = curr_info['row' + str(i)]

                row = [','.join(self._cleanse_list(x.get('column.values', []))) for x in curr_row]
                rows.append(row)

                columns = [x.get('column.display_name', 'Column # {0}'.format(i)) for x in curr_row]

            action_result.set_summary({TANIUM_JSON_ENTRIES_FOUND: len(rows)})

            action_result.add_data({TANIUM_JSON_COLUMNS: columns, TANIUM_JSON_ROWS: rows})

            return action_result.set_status(phantom.APP_SUCCESS)

    def _parse_status_list(self, status_key, status_list):

        # The key will not be Verified or Failed, but instead something like XX:Verified.
        # Lots of extra characters that we don't need, also not too sure about the format,
        # it might not be that formal, so we just loop from a list of well known status texts
        status_texts = ['Expired', 'Failed', 'NotSucceeded', 'Stopped', 'Succeeded', 'Completed', 'Verified', 'Waiting', 'PendingVerification', 'Downloading', 'Copying', 'Running']

        if (not status_list):
            return ''

        status_text_value = None

        for status_text in status_texts:
            if (status_text in status_key):
                status_text_value = status_text
                break

        if (not status_text_value):
            return ''

        status_string = "{0}\n{1}\n".format(status_text_value, ','.join(status_list))

        return status_string

    def _parse_status_response(self, action_results_map, status_key):

        status_str = ''

        status_dict = action_results_map.get(status_key)

        if (not status_dict):
            return (0, status_str)

        total = status_dict.get('total')

        if (not total):
            return (0, status_str)

        for k, v in status_dict.iteritems():
            status_str += self._parse_status_list(k, v)

        return (total, status_str)

    def _parse_deploy_action_response(self, response, action_result):

        progress_str = ''

        try:
            progress_str = response['poller_object'].progress_str
        except:
            pass

        action_result_map = response.get('action_result_map')
        action_object = response.get('action_object', None)

        try:
            action_id = action_object.id
        except:
            action_id = 'unknown'

        if (not action_result_map):
            action_result.set_status(phantom.APP_ERROR,
                    "Did not get detail results from Tanium.{0}".format(" Progress from server: {0}".format(progress_str) if progress_str else ''))

        status = phantom.APP_ERROR

        status_msg = []

        if (progress_str):
            status_msg.append(progress_str)

        total, message = self._parse_status_response(action_result_map, "failed")
        if (total):
            status = phantom.APP_ERROR
        if (message):
            if (message not in status_msg):
                status_msg.append(message)

        total, message = self._parse_status_response(action_result_map, "finished")
        if (total):
            status = phantom.APP_SUCCESS
        if (message):
            if (message not in status_msg):
                status_msg.append(message)

        total, message = self._parse_status_response(action_result_map, "running")
        if (total):
            status = phantom.APP_SUCCESS
        if (message):
            if (message not in status_msg):
                status_msg.append(message)

        total, message = self._parse_status_response(action_result_map, "success")
        if (total):
            status = phantom.APP_SUCCESS
        if (message):
            if (message not in status_msg):
                status_msg.append(message)

        action_result.set_status(status, '\n'.join(status_msg))
        action_result.add_data(action_result_map)
        action_result.set_summary({'id': str(action_id)})

        return phantom.APP_SUCCESS

    def _ask_manual_question(self, sensors, question_filters, action_result):

        rows = []
        columns = []

        ret_val, handler = self._create_handler(action_result)

        if (phantom.is_fail(ret_val)):
            return (action_result.get_status(), rows, columns)

        kwargs = {}
        kwargs["refresh_data"] = True
        kwargs["qtype"] = u'manual'
        kwargs["question_filters"] = question_filters
        kwargs["sensors"] = sensors

        # kwargs["callback"] = {'ProgressChanged': self._question_progress}

        self.save_progress("Querying Tanium")

        try:
            response = handler.ask(**kwargs)
        except Exception as e:
            return (action_result.set_status(phantom.APP_ERROR, "Error while handling question", e), rows, columns)

        results = response.get('question_results')

        if (not response):
            return (action_result.set_status(phantom.APP_ERROR, "Query did not return any results"), rows, columns)

        # call the export_obj() method to convert response to JSON and store it in out
        export_kwargs = {}
        export_kwargs['obj'] = results
        export_kwargs['export_format'] = 'json'

        self.save_progress("Processing response")

        try:
            query_text = response['question_object'].query_text
        except:
            query_text

        try:
            result_infos = handler.export_obj(**export_kwargs)
        except Exception as e:
            return (action_result.set_status(phantom.APP_ERROR, "Unable to parse the response as JSON", e), rows, columns)

        self.debug_print("result_infos", result_infos)

        try:
            result_infos = json.loads(result_infos)
        except Exception as e:
            return (action_result.set_status(phantom.APP_ERROR, "Unable to parse the response info as JSON", e), rows, columns)

        # columns is a list
        columns = []

        # rows is a list of rows, where each row is a list of column values
        rows = []

        for i, curr_info in enumerate(result_infos):

            curr_row = curr_info['row' + str(i)]

            # row = [','.join(x['column.values']) for x in curr_row]
            row = [','.join(self._cleanse_list(x.get('column.values', []))) for x in curr_row]
            rows.append(row)

            columns = [x['column.display_name'] for x in curr_row]

        if (query_text):
            action_result.update_summary({TANIUM_JSON_QUERY_TEXT: query_text})

        return (phantom.APP_SUCCESS, rows, columns)

    def _execute_action(self, param):

        action_result = self.add_action_result(ActionResult(dict(param)))
        container_id = self.get_container_id()
        ip_hostname = param[phantom.APP_JSON_IP_HOSTNAME]
        package_name = param['package_name']
        action_name = "Phantom Execution - %s " % (package_name.split('{')[0].strip())
        endpoint_filter = IP_ACTION_FILTER.format(ip_hostname=ip_hostname)

        if (not phantom.is_ip(ip_hostname)):
            endpoint_filter = MACHINE_NAME_ACTION_FILTER.format(ip_hostname=ip_hostname)

        action_result.set_status(phantom.APP_SUCCESS, "Endpoint Filter: " + str(endpoint_filter))

        self._deploy_action(endpoint_filter, package_name, action_name, ACTION_COMMENT.format(container_id=container_id), action_result)

        return action_result.get_status()

    def _deploy_action(self, action_filters, package, name, comment, action_result):

        ret_val, handler = self._create_handler(action_result)

        if (phantom.is_fail(ret_val)):
            return (ret_val, None)

        # setup the arguments for the handler() class
        kwargs = {}
        kwargs["run"] = True
        kwargs["action_filters"] = action_filters
        kwargs["package"] = package
        kwargs["action_name"] = name
        kwargs["action_comment"] = comment

        self.save_progress("Deploying Action on Tanium")

        try:
            response = handler.deploy_action(**kwargs)
        except Exception as e:
            return action_result.set_status(phantom.APP_ERROR, "Error while deploying action", e)

        self._parse_deploy_action_response(response, action_result)

        return phantom.APP_SUCCESS

    def _test_connectivity(self, param):

        # Progress
        self.save_progress(TANIUM_USING_BASE_URL, base_url=self._base_url)

        config = self.get_config()

        # Connectivity
        self.save_progress(phantom.APP_PROG_CONNECTING_TO_ELLIPSES, config[phantom.APP_JSON_DEVICE])

        ret_val, handler = self._create_handler(result_obj=self)

        if (phantom.is_fail(ret_val)):
            self.append_to_message(TANIUM_ERR_CONNECTIVITY_TEST)
            return self.get_status()

        return self.set_status_save_progress(phantom.APP_SUCCESS, TANIUM_SUCC_CONNECTIVITY_TEST)

    def _terminate_process(self, param):

        action_result = self.add_action_result(ActionResult(dict(param)))
        container_id = self.get_container_id()
        proc_name = param[phantom.APP_JSON_NAME]
        ip_hostname = param[phantom.APP_JSON_IP_HOSTNAME]
        endpoint_filter = IP_ACTION_FILTER.format(ip_hostname=ip_hostname)

        if (not phantom.is_ip(ip_hostname)):
            endpoint_filter = MACHINE_NAME_ACTION_FILTER.format(ip_hostname=ip_hostname)

        self._deploy_action(endpoint_filter, KILL_PROC_PACKAGE.format(proc_name=proc_name), ACTION_NAME_TERM_PROC, ACTION_COMMENT.format(container_id=container_id), action_result)

        return action_result.get_status()

    def _reboot_system(self, param):

        action_result = self.add_action_result(ActionResult(dict(param)))
        container_id = self.get_container_id()
        ip_hostname = param[phantom.APP_JSON_IP_HOSTNAME]
        endpoint_filter = IP_ACTION_FILTER.format(ip_hostname=ip_hostname)

        if (not phantom.is_ip(ip_hostname)):
            endpoint_filter = MACHINE_NAME_ACTION_FILTER.format(ip_hostname=ip_hostname)

        self._deploy_action(endpoint_filter, REBOOT_SYS_PACKAGE, ACTION_NAME_REBOOT_SYS, ACTION_COMMENT.format(container_id=container_id), action_result)

        return action_result.get_status()

    def _list_processes(self, param):

        action_result = self.add_action_result(ActionResult(param))

        ret_val, handler = self._create_handler(action_result)

        if (phantom.is_fail(ret_val)):
            return action_result.get_status()

        # setup the arguments for the handler() class
        ip_hostname = param[phantom.APP_JSON_IP_HOSTNAME]
        endpoint_filter = IP_ACTION_FILTER.format(ip_hostname=ip_hostname)

        if (not phantom.is_ip(ip_hostname)):
            endpoint_filter = MACHINE_NAME_ACTION_FILTER.format(ip_hostname=ip_hostname)

        ret_val, rows, columns = self._ask_manual_question(['Running Processes'], [endpoint_filter], action_result)

        if (not ret_val):
            return action_result.get_status()

        action_result.update_summary({TANIUM_JSON_ENTRIES_FOUND: len(rows)})

        # Format the output
        [action_result.add_data({'name': x[0], 'count': x[1]}) for x in rows]

        return action_result.set_status(phantom.APP_SUCCESS)

    def _get_parsed_questions(self, param):

        # Create the action result to have something to add to when we get data later.
        action_result = self.add_action_result(ActionResult(param))

        # Create a handler with all the necessary fields to be sent through the request
        ret_val, handler = self._create_handler(action_result)

        if (phantom.is_fail(ret_val)):
            return action_result.get_status()

        # Just trying to be helpful
        self.save_progress("Building parameters")

        kwargs = {}
        kwargs["refresh_data"] = True
        kwargs["qtype"] = u'parsed'
        kwargs["question_text"] = param[TANIUM_JSON_QUESTION]
        kwargs["callback"] = {'ProgressChanged': self._question_progress}

        try:
            response = handler.parse_query(**kwargs)
        except Exception as e:
            return action_result.set_status(phantom.APP_ERROR, "Error while getting questions", e)

        try:
            for index, resp in enumerate(response):
                action_result.add_data({"question": {"question_text": resp.question_text, "score": resp.score, "index": index}})
                action_result.set_summary({"total_objects": len(response)})
        except Exception as e:
            return action_result.set_status(phantom.APP_ERROR, "Error while parsing response", e)

        return action_result.set_status(phantom.APP_SUCCESS)

    def _ask_parsed_question(self, param):

        action_result = self.add_action_result(ActionResult(param))

        ret_val, handler = self._create_handler(action_result)

        if (phantom.is_fail(ret_val)):
            return action_result.get_status()

        # setup the arguments for the handler() class
        ques_name = param[TANIUM_JSON_QUESTION]

        kwargs = {}
        kwargs["refresh_data"] = True
        kwargs["qtype"] = u'parsed'
        kwargs["question_text"] = ques_name
        kwargs["callback"] = {'ProgressChanged': self._question_progress}
        kwargs["picker"] = 1

        self.save_progress("Querying Tanium")

        try:
            response = handler.ask(**kwargs)
        except Exception as e:
            return action_result.set_status(phantom.APP_ERROR, "Error while getting questions", e)

        results = response.get('question_results')

        if (not results):
            return action_result.set_status(phantom.APP_ERROR, "Query did not return any results")

        # call the export_obj() method to convert response to JSON and store it in out
        export_kwargs = {}
        export_kwargs['obj'] = results
        export_kwargs['export_format'] = 'json'

        self.save_progress("Processing response")

        try:
            result_infos = handler.export_obj(**export_kwargs)
        except Exception as e:
            return action_result.set_status(phantom.APP_ERROR, "Unable to parse the response as JSON", e)

        self.debug_print("result_infos", result_infos)

        # Test if the query that was actually run is the same that was input
        if (ques_name.lower() != response.get('parse_results')[0].question_text.lower()):
            return action_result.set_status(phantom.APP_ERROR, "Could not find the specified parsed question.")

        try:
            result_infos = json.loads(result_infos)
        except Exception as e:
            return action_result.set_status(phantom.APP_ERROR, "Unable to parse the response info as JSON", e)

        # columns is a list
        columns = []

        # rows is a list of rows, where each row is a list of column values
        rows = []

        for i, curr_info in enumerate(result_infos):
            curr_row = curr_info['row' + str(i)]

            row = [','.join(self._cleanse_list(x.get('column.values', []))) for x in curr_row]
            rows.append(row)

            columns = [x.get('column.display_name', 'Column # {0}'.format(i)) for x in curr_row]

        action_result.set_summary({TANIUM_JSON_ENTRIES_FOUND: len(rows)})

        action_result.add_data({TANIUM_JSON_COLUMNS: columns, TANIUM_JSON_ROWS: rows})

        return action_result.set_status(phantom.APP_SUCCESS)

    def handle_action(self, param):

        result = None
        action = self.get_action_identifier()

        if (action == self.ACTION_ID_LIST_SAVED_QUESTIONS):
            result = self._list_saved_questions(param)
        elif (action == self.ACTION_ID_EXECUTE_SAVED_QUESTION):
            result = self._ask_saved_question(param)
        elif (action == self.ACTION_ID_REBOOT_SYSTEM):
            self._reboot_system(param)
        elif (action == self.ACTION_ID_TERM_PROCESS):
            self._terminate_process(param)
        elif (action == phantom.ACTION_ID_TEST_ASSET_CONNECTIVITY):
            result = self._test_connectivity(param)
        elif (action == self.ACTION_ID_LIST_PROCESSES):
            result = self._list_processes(param)
        elif (action == self.ACTION_ID_EXECUTE_CUSTOM_QUESTION):
            result = self._get_parsed_questions(param)
        elif (action == self.ACTION_ID_EXECUTE_ACTION):
            result = self._execute_action(param)
        else:
            self.unknown_action()

        return result


if __name__ == '__main__':

    import sys
    import pudb
    pudb.set_trace()

    if (len(sys.argv) < 2):
        print "No test json specified as input"
        exit(0)

    with open(sys.argv[1]) as f:
        in_json = f.read()
        in_json = json.loads(in_json)
        print(json.dumps(in_json, indent=4))

        connector = TaniumConnector()
        connector.print_progress_message = True
        ret_val = connector._handle_action(json.dumps(in_json), None)
        print ret_val

    exit(0)
