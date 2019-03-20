# File: tanium_view.py
# Copyright (c) 2016-2019 Splunk Inc.
#
# SPLUNK CONFIDENTIAL - Use or disclosure of this material in whole or in part
# without a valid written license from Splunk Inc. is PROHIBITED.

from tanium_consts import *
from phantom.json_keys import *


def get_ctx_result(provides, result):
    """ Function that parses data.

    :param result: result
    :param provides: action name
    :return: response data
    """

    ctx_result = {}

    param = result.get_param()
    summary = result.get_summary()
    data = result.get_data()

    ctx_result['action'] = provides
    ctx_result['param'] = param

    if summary:
        ctx_result['summary'] = summary

    if not data:
        ctx_result['data'] = {}
        return ctx_result

    results_dict = {}
    results_dict['column_headers'] = data[0].get(TANIUM_JSON_COLUMNS)

    # List of result values for a given row
    column_values = []

    data_rows = data[0].get(TANIUM_JSON_ROWS)
    for data_row in data_rows:
        new_row = []
        for value in data_row:
            if isinstance(value, list):
                value = ', '.join(value)
            new_row.append(value)
        column_values.append(new_row)

    results_dict['column_values'] = column_values

    ctx_result['data'] = results_dict

    return ctx_result


def tanium_ques_results(provides, all_results, context):

    context['results'] = results = []
    for summary, action_results in all_results:
        for result in action_results:

            ctx_result = get_ctx_result(provides, result)
            if not ctx_result:
                continue
            results.append(ctx_result)

    return 'tanium_run_query.html'
