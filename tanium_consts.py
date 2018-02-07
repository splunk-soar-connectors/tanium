# --
# File: tanium_consts.py
#
# Copyright (c) Phantom Cyber Corporation, 2014-2018
#
# This unpublished material is proprietary to Phantom Cyber.
# All rights reserved. The methods and
# techniques described herein are considered trade secrets
# and/or confidential. Reproduction or distribution, in whole
# or in part, is forbidden except by express written permission
# of Phantom Cyber.
#
# --

# Json keys specific to the app's input parameters/config and the output result
TANIUM_JSON_TOTAL_SAVED_QUESTS = "total_saved_questions"
TANIUM_JSON_QUESTION = "query"
TANIUM_JSON_COLUMNS = "columns"
TANIUM_JSON_ROWS = "rows"
TANIUM_JSON_ENTRIES_FOUND = "number_of_results_found"
TANIUM_JSON_QUERY_TEXT = "query_text"
TANIUM_JSON_PARSED_FLAG = "is_parsed"

# Status messages for the app
TANIUM_SUCC_CONNECTIVITY_TEST = "Connectivity test passed"
TANIUM_ERR_CONNECTIVITY_TEST = "Connectivity test failed"
TANIUM_ERR_UNABLE_TO_PARSE_REPLY = "Unable to parse reply from server"
TANIUM_ERR_SOAP_API_FAILED = "Soap API failed"
TANIUM_ERR_UNABLE_TO_PARSE_RESULT_XML = "Unable to parse the result xml from server"
TANIUM_SUCC_GOT_EMPTY_RESULT = "Got empty results from server. No data to show"
TANIUM_ERR_PACKAGE_DETAILS = "Unable to get details about package '{package}' required to execute the action"
TANIUM_ERR_SERVER_CONNECTION = "Connection to server error"
TANIUM_ERR_REPLY_KEYS_MISSING = "Mandatory keys missing in response, can't parse"

# Progress messages format string
TANIUM_USING_BASE_URL = "Using base url: {base_url}"
TANUIM_GOT_PACKAGE_ID = "Got package id '{id}' for '{package}'"

# Other constants used in the connector

MACHINE_NAME_ACTION_FILTER = "Computer Name, that equals:{ip_hostname}"
IP_ACTION_FILTER = "IP Address, that equals:{ip_hostname}"
KILL_PROC_PACKAGE = "Kill Process - ||Running Processes||{{||Running Processes||={proc_name}}}"
REBOOT_SYS_PACKAGE = "Reboot Windows Machine{$1=no,$2=5}"
ACTION_NAME_TERM_PROC = "Phantom Terminate Process Action"
ACTION_NAME_REBOOT_SYS = "Phantom Reboot System Action"
ACTION_COMMENT = "Action performed for container id: {container_id}"
TANIUM_PARSED_FLAG_DEF_VALUE = False
