# File: tanium_view.py
# Copyright (c) 2015-2018 Splunk Inc.
#
# SPLUNK CONFIDENTIAL – Use or disclosure of this material in whole or in part
# without a valid written license from Splunk Inc. is PROHIBITED.

from tanium_consts import *
from phantom.json_keys import *


def tanium_ques_results(provides, all_results, context):

    context['rows'] = rows = []

    for summary, action_results in all_results:
        for result in action_results:
            parameter = result.get_param()
            context['title1'] = "{0}".format(parameter.get(TANIUM_JSON_QUESTION, ''))
            context['title2'] = 'Results'

            data = result.get_data()
            if (data is None) or (len(data) == 0):
                continue

            context['headers'] = data[0][TANIUM_JSON_COLUMNS]
            data_rows = data[0][TANIUM_JSON_ROWS]
            for data_row in data_rows:
                new_row = []
                rows.append(new_row)
                for value in data_row:
                    if isinstance(value, list):
                        value = ', '.join(value)
                    new_row.append({'value': value})

    return '/widgets/generic_table.html'
