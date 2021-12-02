[comment]: # " File: readme.md"
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
