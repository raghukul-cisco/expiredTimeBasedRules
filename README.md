# expiredTimeBasedRules

This API based tool helps in detecting time based rules that have expired from the Access Control Policy on FMC. Currently there is no option available in the GUI of FMC to identify the time based rules which are expired.

In addition to the detection of expired time based rules, the tool also provides the user with the option to either disable the rule, delete the rule or skip the remediation all together.

![add-image-here]()
 
## Use Case Description

This API based tool helps in detecting time based rules that have expired from the Access Control Policy on FMC. Currently there is no option available in the GUI of FMC to identify the time based rules which are expired.

In addition to the detection of expired time based rules, the tool also provides the user with the option to either disable the rule, delete the rule or skip the remediation all together.

## Installation

Requirements for installation:

pip3 install fireREST
pip3 install netaddr
pip3 install datetime
pip3 install ipaddress
pip3 install xlsxwriter

Or alternatively you can the command below to download dependencies via the requirements.txt file, this has to be executed from the downloaded script directory.

pip3 install -r ./requirements.txt


## Usage

Once the dependencies are installed and the code is pulled from GitHub, it is good to go. Below mentioned are the steps to follow in order to execute it:

First thing to ensure is, the machine where the code will be installed should have connectivity with the FMC under concern.
It is recommended to create a different user for the tool, so that it does not block existing users from logging into the FMC for operational changes.
Navigate to the location where the script is installed.
In order to execute the script, run the below command:

Step 1:Once the credentials are entered, the script connects to the FMC and provides the list of Access Control Policy that are available in Global Domain.


Now, the policies listed are case sensitive. Hence, while choosing the ACP which has to be exported the user can enter one of three possibilities:

Name of a single ACP (case sensitive) and press return.
Comma seperated ACP names in case multiple ACP have to process and press return. (All the ACP names should be case sensitive)
Default behavior with just return pressed. (All the ACP available/listed would be processed)

Step 2:Once the ACP's are selected, users will be asked with 3 options:

Enter 'delete'/'Delete' and press return: Rules in the selected ACP's will be deleted and report generation.
Enter 'disable'/'Disable' and press return: Rules in the selected ACP's will be disabled and report generation
Default behavior with just return pressed: Generation excel report on expired rules without taking any action on rules.


Once the above option is selected, the script will execute the selected action on ACP's.

Example:

python3 expiredTimeBasedRules.py 
	Enter the IP Address of the FMC:
	Enter the username for the FMC:  
	Enter the password associated with the username entered: 
 
ACP available in global domain: 
		Name: timebased_policy
		Name: timebased_2_policy


Enter the ACP Name (case sensitive) if you want specific check for specific ACP (multiple values should be comma seperated). By default all the ACP would be checked, press return for default behaviour: 
 

*********************************

Enter 'delete' to delete Expired rules
Enter 'disable' to disable Expired rules
or Enter anything to continue with just reports:  

Inside Object Pull
Inside time based validation
Inside ACP
Successfully Written rule 1 of timebased_policy
Successfully Written rule 3 of timebased_2_policy

Output Generated:

	1.The excel sheet will be generated in the same folder with expired rules info in it.
	2.The name of the excelsheet generated is "detailed_report.xlsx"
	3.In case of multiple ACP being entered or default behavior, the ACP is processed in sequential order similar to policies listed after we enter the credentials for the script.
	4.On FMC 'disbale' / 'delete' action will be taken based on option selection in Step 2.
	5.The output on console displays the expired rule number in ACP that is written to excel sheet.


### DevNet Sandbox

DevNet Learning Lab Please go to the DevNet Learning Lab for Firepower Management Center (FMC) to learn how to use these scripts: https://developer.cisco.com/learning/modules/fmc-api

DevNet Sandbox The Sandbox which can implement this script is at: https://devnetsandbox.cisco.com/RM/Diagram/Index/1228cb22-b2ba-48d3-a70a-86a53f4eecc0?diagramType=Topology

## Known issues

Document any significant shortcomings with the code. If using [GitHub Issues](https://help.github.com/en/articles/about-issues) to track issues, make that known and provide any templates or conventions to be followed when opening a new issue. 

## Getting help

Instruct users how to get help with this code; this might include links to an issues list, wiki, mailing list, etc.

**Example**

If you have questions, concerns, bug reports, etc., please create an issue against this repository.

## Author(s)

This project was written and is maintained by the following individuals:

* Nikhil Alampalli Ramu <nalampal@cisco.com>
* Raghunath Kulkarni <raghukul@cisco.com>
