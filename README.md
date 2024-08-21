[comment]: # "Auto-generated SOAR connector documentation"
# Tanium

Publisher: Splunk  
Connector Version: 1.2.42  
Product Vendor: Tanium  
Product Name: Tanium  
Product Version Supported (regex): ".\*"  
Minimum Product Version: 4.0.1068  

This app supports investigative and containment actions on Tanium

[comment]: # " File: README.md"
[comment]: # "  Copyright (c) 2016-2019 Splunk Inc."
[comment]: # ""
[comment]: # "Licensed under the Apache License, Version 2.0 (the 'License');"
[comment]: # "you may not use this file except in compliance with the License."
[comment]: # "You may obtain a copy of the License at"
[comment]: # ""
[comment]: # "    http://www.apache.org/licenses/LICENSE-2.0"
[comment]: # ""
[comment]: # "Unless required by applicable law or agreed to in writing, software distributed under"
[comment]: # "the License is distributed on an 'AS IS' BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,"
[comment]: # "either express or implied. See the License for the specific language governing permissions"
[comment]: # "and limitations under the License."
[comment]: # ""
**Notes**

-   The asset configuration parameter **port** is optional, if not specified the app will use 443.
    Depending on the Tanium server version, other valid values can be 8443 or 444.
-   Actions like **terminate process** and **reboot system** work on either an ip address or a host
    name.
-   It has been noticed that Tanium requires the host name to be an FQDN like
    win7ult32.corp.contoso.com instead of just win7ult32.

**Timeout Parameter Guidelines**

-   Default expiry of any question asked on the Tanium server is 10 minutes. If the action is run
    with invalid parameters and timeout parameter is not specified, the action won't terminate
    immediately and will take 10 minutes for getting completed. Hence, timeout parameter has been
    made mandatory in all actions to avoid such a situation.
-   Default timeout of any action supporting it on the Tanium app is 60 seconds. This timeout has
    been decided after considering the worst case requiring to load a huge output data response.
    User needs to provide a timeout based on their requirements for the action execution.
-   Default timeout of any action supporting it on the Tanium app is 60 seconds

**Run Query Guidelines**

-   Two modes of operation are supported for run query action

      

    1.  Saved Questions - User can save a manually created question on the Tanium server and then,
        provide the name of that saved question in the query parameter to fetch appropriate results.
        **is_parsed** parameter has to be set to False for this to work correctly.
    2.  Manual Questions - User can directly provide the question to be asked to the Tanium server
        in the query parameter to fetch appropriate results. **is_parsed** parameter has to be set
        to True for this to work correctly.

**Terminate Process Guidelines**

-   Please follow the below steps to execute this action successfully

      

    1.  Create and save a package on the Tanium server with a meaningful package name and add a
        command to terminate the required process in the package's command section
    2.  Create and save a sensor on the Tanium server with a meaningful name and add a valid script
        code for fetching all the running processes for the authenticated user
    3.  Run the action **Terminate Process** with valid parameters and using the package and sensor
        name created in the above steps.

**Reboot System and Execute Action Guidelines**

-   Please follow the below steps to execute this action successfully

      

    1.  Create and save a package on the Tanium server with a meaningful package name and add a
        command to reboot the system in the package's command section
    2.  Run the action **Reboot System or Execute Action** with valid parameters and using the
        package name created in the above step.

-   On a successful action run on Phantom, this will launch an action on the Tanium server and will
    execute the command mentioned in the package linked with the launched action


### Configuration Variables
The below configuration variables are required for this Connector to operate.  These variables are specified when configuring a Tanium asset in SOAR.

VARIABLE | REQUIRED | TYPE | DESCRIPTION
-------- | -------- | ---- | -----------
**device** |  required  | string | Device IP/Hostname
**port** |  optional  | string | Port
**username** |  required  | string | Username
**password** |  required  | password | Password
**verify_server_cert** |  optional  | boolean | Verify server certificate

### Supported Actions  
[test connectivity](#action-test-connectivity) - Validate the asset configuration for connectivity using supplied configuration  
[list questions](#action-list-questions) - List the saved questions on the box  
[run query](#action-run-query) - Run a saved or parsed question  
[execute action](#action-execute-action) - Execute Tanium action (package)  
[reboot system](#action-reboot-system) - Reboots the system  
[list processes](#action-list-processes) - List the running processes on a machine  
[terminate process](#action-terminate-process) - Terminate a process  
[manual query](#action-manual-query) - Ask a Manual question without parsing  
[parse question](#action-parse-question) - Retrieves related questions to a possible Tanium question  

## action: 'test connectivity'
Validate the asset configuration for connectivity using supplied configuration

Type: **test**  
Read only: **True**

#### Action Parameters
No parameters are required for this action

#### Action Output
No Output  

## action: 'list questions'
List the saved questions on the box

Type: **investigate**  
Read only: **True**

#### Action Parameters
No parameters are required for this action

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success 
action_result.data.\*.id | string |  |   1 
action_result.data.\*.name | string |  `tanium question`  |   Has Tanium Standard Utilities 
action_result.data.\*.query_text | string |  |   Get Has Tanium Standard Utilities from all machines 
action_result.summary.total_saved_questions | numeric |  |   97 
action_result.message | string |  |   Total saved questions: 97 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'run query'
Run a saved or parsed question

Type: **investigate**  
Read only: **True**

<p>The <b>run query</b> action can be used to run either a saved question or a parsed question.</p><p>A saved question is a commonly asked question that had been saved by any of the operators on the Tanium platform.  Saved questions can be ones that Tanium added by default or custom questions that operators on the Tanium platform regularly use.</p><p>A parsed question is a little more complex.  The Tanium platform will not process questions unless they are saved by an operator on the platform, or is one of the default Tanium questions.  But thankfully, Tanium, when asked a non-saved question, will parse the question it is given, and give a list of suggestions that are related to the question it's given.</p><p>For example, on the Tanium platform, if one were to just ask the question, 'all IP addresses,' Tanium will give the suggestions:<br><ul><li>Get Static IP Addresses from all machines</li><li>Get IP Routes from all machines</li><li>Get IP Address from all machines</li><li>Get IP Connections from all machines</li><li>Get IP Route Details from all machines</li><li>Get Network IP Gateway from all machines</li></ul><br>Tanium sorts this list, from most-related to least-related.  That is, the option at the top of the list, which in this case is 'Get Static IP Addresses from all machines', is considered most-related to the given question 'all ip addresses.'<br>This functionality is reflected in the action <b>parse question</b>.</p><p>When the <b>is_parsed</b> box is checked (by default, it is not), the '<b>run query</b>' action behaves differently.  Instead of considering the question as a 'saved question', it will first ask the Tanium platform to return a list of the questions related to the one it is given.  It will then choose the most-related question from the list (the one at the top), and run that question.</p><p>Chaining results from the <b>parse question</b> action are highly recommended.  Questions in the action result of <b>parse question</b> are, not surprisingly, already parsed. As a result, using the <b>run query</b> on a parsed question will ensure that the top result in the list is the question that is given.</p><p>For example, giving the <b>query</b> 'all IP addresses' to the <b>parse question</b> will return the same list as above in an action result.  Similarly, giving the parsed query 'Get Static IP Addresses from all machines' to <b>parse question</b> will have 'Get Static IP Addresses from all machines' at the top as well.</p><p>By parsing the question Tanium is given, Tanium gives back questions that it knows it will understand.  And by giving Tanium a question that it knows it will understand (by using <b>parse question</b>), using the <b>run query</b> action with the <b>is_parsed</b> option checked/True, Tanium will be guaranteed to run the question, without having to save it.</p>

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**query** |  required  | Saved question to execute | string |  `tanium question`  `tanium parsed question` 
**is_parsed** |  optional  | Parsed question | boolean | 
**timeout_seconds** |  required  | If supplied and not 0, timeout in seconds instead of when object expires | numeric | 
**ip_hostname** |  required  | Hostname/IP to run query on | string |  `ip`  `host name` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success 
action_result.parameter.ip_hostname | string |  `ip`  `host name`  |   10.1.18.132 
action_result.parameter.is_parsed | boolean |  |   False  True 
action_result.parameter.query | string |  `tanium question`  `tanium parsed question`  |   BIOS Information 
action_result.parameter.timeout_seconds | numeric |  |   300 
action_result.data.\*.columns | string |  |   Count 
action_result.data.\*.rows | string |  |  
action_result.data.\*.rows.\* | string |  |   2 
action_result.summary.number_of_results_found | numeric |  |   1 
action_result.message | string |  |   Number of results found: 1 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'execute action'
Execute Tanium action (package)

Type: **generic**  
Read only: **False**

Use this action to run packages on endpoints. You will be required to know the Package name and the parameters to pass.<br>For example the <b>Registry - Create Key</b> package is used to create a Registry key on an endpoint. It takes two parameters<ul><li><b>$1</b> is the Architecture</li> and <li><b>$2</b> is the Registry Key Name</li></ul>So use the <b>execute action</b> with the <b>package_name</b> set to:<br><b>Registry - Create Key{$1=64,$2=HKLM\\Software\\Phantom\\TestKey}</b><br>The Tanium UI displays the documentation of the package, its name, and parameters.<br>The action behavior depends a lot on the package used. In most cases the action status pertains to if the package was executed or not, i.e. the Tanium API will treat the execution of the package as successful. For instance, in the above example, $1 specifies the architecture and $2 is the key to create. If the HKLM\\Software\\Phantom key is not present in the HKLM hive, the package will fail to create the HKLM\\Software\\Phantom\\TestKey key, however, the API will return a success since an attempt was made.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**ip_hostname** |  required  | Hostname/IP of machine to run action on | string |  `ip`  `host name` 
**package_name** |  required  | Name of Tanium package | string |  `tanium package name` 
**action_group** |  required  | Action Group to execute on | string |  `tanium action group` 
**timeout_seconds** |  required  | If supplied and not 0, timeout in seconds instead of when object expires | numeric | 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success 
action_result.parameter.action_group | string |  `tanium action group`  |   WinGroup 
action_result.parameter.ip_hostname | string |  `ip`  `host name`  |   win7ult32.corp.contoso.com 
action_result.parameter.package_name | string |  `tanium package name`  |   Registry - Delete Key{$1=32,$2=HKLM\\Software\\Phantom\\TestKey} 
action_result.parameter.timeout_seconds | numeric |  |   300 
action_result.data | string |  |  
action_result.data.\*.failed.total | numeric |  |   0 
action_result.data.\*.finished.256:Completed. | string |  |   win7ult32.corp.contoso.com 
action_result.data.\*.finished.total | numeric |  |   1 
action_result.data.\*.running.total | numeric |  |   0 
action_result.data.\*.success.256:Completed. | string |  |   win7ult32.corp.contoso.com 
action_result.data.\*.success.total | numeric |  |   1 
action_result.data.\*.unknown.total | numeric |  |   0 
action_result.summary | string |  |  
action_result.summary.id | string |  |   256 
action_result.message | string |  |   failed: 0, finished: 1, running: 0, success: 1, unknown: 0, Done Key: success, Passed Count: 1
Completed
win7ult32.corp.contoso.com
 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'reboot system'
Reboots the system

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**ip_hostname** |  required  | Hostname/IP of machine to reboot | string |  `ip`  `host name` 
**action_group** |  required  | Action Group to execute on | string |  `tanium action group` 
**timeout_seconds** |  required  | If supplied and not 0, timeout in seconds instead of when object expires | numeric | 
**package_name** |  required  | Name of Tanium package | string |  `tanium package name` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success 
action_result.parameter.action_group | string |  `tanium action group`  |   Default 
action_result.parameter.ip_hostname | string |  `ip`  `host name`  |   tanium-01 
action_result.parameter.package_name | string |  `tanium package name`  |   list directories 
action_result.parameter.timeout_seconds | numeric |  |   300  60 
action_result.data | string |  |  
action_result.data.\*.failed.total | numeric |  |   0 
action_result.data.\*.finished.51053:Completed. | string |  |   tanium-01 
action_result.data.\*.finished.total | numeric |  |   1 
action_result.data.\*.running.total | numeric |  |   0 
action_result.data.\*.success.51053:Completed. | string |  |   tanium-01 
action_result.data.\*.success.total | numeric |  |   1 
action_result.data.\*.unknown.total | numeric |  |   0 
action_result.summary | string |  |  
action_result.summary.id | string |  |   51053 
action_result.message | string |  |   failed: 0, finished: 1, running: 0, success: 1, unknown: 0, Done Key: success, Passed Count: 1
Completed
tanium-01
 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'list processes'
List the running processes on a machine

Type: **investigate**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**ip_hostname** |  required  | Hostname/IP to list process on | string |  `ip`  `host name` 
**sensor** |  required  | Name of Tanium sensor | string |  `tanium sensor` 
**timeout_seconds** |  required  | If supplied and not 0, timeout in seconds instead of when object expires | numeric | 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success 
action_result.parameter.ip_hostname | string |  `ip`  `host name`  |   win7ult32.corp.contoso.com 
action_result.parameter.sensor | string |  `tanium sensor`  |   Running Processes With User 
action_result.parameter.timeout_seconds | numeric |  |   300 
action_result.data.\*.count | string |  |   1 
action_result.data.\*.name | string |  `process name`  `file name`  |   TaniumClient.exe 
action_result.summary.number_of_results_found | numeric |  |   36 
action_result.summary.query_text | string |  |   Get Running Processes from all machines with Computer Name = "win7ult32.corp.contoso.com" 
action_result.message | string |  |   Number of results found: 36
Query text: Get Running Processes from all machines with Computer Name = "win7ult32.corp.contoso.com" 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'terminate process'
Terminate a process

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**ip_hostname** |  required  | Hostname/IP to terminate process on | string |  `ip`  `host name` 
**name** |  required  | Name of process to terminate | string |  `file name`  `process name` 
**action_group** |  required  | Action Group to execute on | string |  `tanium action group` 
**timeout_seconds** |  required  | If supplied and not 0, timeout in seconds instead of when object expires (10 min) | numeric | 
**sensor** |  required  | Name of Tanium sensor | string |  `tanium sensor` 
**package_name** |  required  | Name of Tanium package | string |  `tanium package name` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success 
action_result.parameter.action_group | string |  `tanium action group`  |   All Computers 
action_result.parameter.ip_hostname | string |  `ip`  `host name`  |   win7ult32.corp.contoso.com 
action_result.parameter.name | string |  `file name`  `process name`  |   notepad.exe 
action_result.parameter.package_name | string |  `tanium package name`  |   list directories 
action_result.parameter.sensor | string |  `tanium sensor`  |   Running Processes With User 
action_result.parameter.timeout_seconds | numeric |  |   300 
action_result.data | string |  |  
action_result.data.\*.failed.total | numeric |  |   0 
action_result.data.\*.finished.257:Completed. | string |  |   win7ult32.corp.contoso.com 
action_result.data.\*.finished.total | numeric |  |   1 
action_result.data.\*.running.total | numeric |  |   0 
action_result.data.\*.success.257:Completed. | string |  |   win7ult32.corp.contoso.com 
action_result.data.\*.success.total | numeric |  |   1 
action_result.data.\*.unknown.total | numeric |  |   0 
action_result.summary | string |  |  
action_result.summary.id | string |  |   257 
action_result.message | string |  |   failed: 0, finished: 1, running: 0, success: 1, unknown: 0, Done Key: success, Passed Count: 1
Completed
win7ult32.corp.contoso.com
 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'manual query'
Ask a Manual question without parsing

Type: **investigate**  
Read only: **True**

This action takes a human-readable string to in turn ask Tanium a question. The question is broken into three different parameters:<ul><li><b>left_side</b>: This is what you are requesting back from Tanium. This is ingested as a string of options separated by a semicolon (Ex: &quotComputer Name; IP Address&quot would return both Computer names and IP addresses)</li><li><b>right_side</b>: This is the filter to pass to Tanium. Different filters should be separated by a semicolon. (Ex: &quotOperating Systems, that contains Windows; Operating System, that contains:Linux&quot)</li><li><b>query_options</b>: These are the options passed to Tanium. (Ex: &quotand&quot, &quot ) ;or&quot etc...)

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**left_side** |  required  | Tanium Response set | string |  `tanium response` 
**right_side** |  optional  | The filter for the Tanium question | string |  `tanium filter` 
**query_options** |  optional  | Options for Tanium question | string |  `tanium options` 
**timeout_seconds** |  required  | If supplied and not 0, timeout in seconds instead of when object expires | numeric | 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success 
action_result.parameter.left_side | string |  `tanium response`  |   Computer Name;IP Address 
action_result.parameter.query_options | string |  `tanium options`  |   or 
action_result.parameter.right_side | string |  `tanium filter`  |   Operating System, that contains:Windows; Operating System, that contains:Linux 
action_result.parameter.timeout_seconds | numeric |  |   300 
action_result.data.\*.count | string |  |  
action_result.data.\*.name | string |  |  
action_result.summary.number_of_results_found | numeric |  |   7 
action_result.summary.query_text | string |  |   Get Computer Name and IP Address from all machines with ( Operating System containing "Windows" or Operating System containing "Linux" ) 
action_result.message | string |  |   Number of results found: 7
Query text: Get Computer Name and IP Address from all machines with ( Operating System containing "Windows" or Operating System containing "Linux" ) 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'parse question'
Retrieves related questions to a possible Tanium question

Type: **investigate**  
Read only: **True**

<p>The <b>parse question</b> action is what allows the use of custom queries.  Tanium itself does not accept custom queries, and will instead provide suggestions on pre-made queries that Tanium will accept.  The action result contains <b>question_text</b>, which are essentially Tanium-approved questions whose structure best match the query that was given.  The <b>question_text</b> is given the data type of <b>tanium parsed question</b>.  This allows contextual actions to be taken so that the questions can then be used in the <b>run query</b>.</p><p>The order of the <b>question_text</b> within the action output is very important.  Tanium scores each parsed question based upon how much it matches the given query.  That is, the higher the score that Tanium has given, the higher it will appear in the list.  Each question in the list is given an index as well.  For example, if given 'ip addresses', Tanium decides that 'Get IP Address from all machines' is the most related - giving it a score of 6031 and an index of 0.  Similarly, the Tanium decides that, though related to 'ip address', the question 'Get Static IP Addresses from all machines' will have a score of 120 and an index of 10.</p>

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**query** |  required  | Query to find related questions for | string |  `tanium question`  `tanium parsed question` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success 
action_result.parameter.query | string |  `tanium question`  `tanium parsed question`  |   Count 
action_result.data.\*.question.index | numeric |  |   0 
action_result.data.\*.question.question_text | string |  `tanium parsed question`  |   Get Tanium Buffer Count from all machines 
action_result.data.\*.question.score | numeric |  |   5541 
action_result.summary | string |  |  
action_result.summary.total_objects | numeric |  |   5 
action_result.message | string |  |   Total objects: 5 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1 