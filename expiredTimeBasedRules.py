import re
import getpass
import sys
import warnings
import requests
import time
import json
from fireREST import FMC
from netaddr import *
import ipaddress
import datetime
import xlsxwriter

trObjects = {}
expired = []
forever = []
expiredRules = {}

#initialize xcel sheet parameters

workbook = xlsxwriter.Workbook('detailed_report.xlsx')
worksheet = workbook.add_worksheet()
worksheet.set_column('A:D', 15)
style4=workbook.add_format({'align':'center', 'border':1 })
style1 = workbook.add_format({'bold': True,'align' : 'center' ,'fg_color' : 'yellow' , 'border_color' : 'black', 'border':1})
row = 0
column = 0
heading= ['Policy','Rule_Id', 'Rule_Name', 'Expired_date']
for i in heading:
    worksheet.write(row, column, i , style1)
    column += 1
row=1
#

def objectGuide(fmc):
	print ("Inside Object Pull")
	timeRange = fmc.object.timerange.get()

	for item in timeRange:
		temp = item['effectiveEndDateTime'].split("T")
		trObjects[item['name']] =  temp

	timeBaseValidation()

def timeBaseValidation():
	print ("Inside time based validation")

	now = datetime.datetime.now()
	now = str(now).split(" ")
	now = time.strptime(now[0], "%Y-%m-%d")
	for key,value in trObjects.items():
		if ("Never End" in value):
			forever.append(key)
		else:
			configured = time.strptime(value[0], "%Y-%m-%d")
			if (configured < now):
				expired.append(key)


def getInput():
	
	hostname = input("Enter the IP Address of the FMC: ")
	username = input("Enter the username for the FMC: ")
	password = getpass.getpass("Enter the password associated with the username entered: ")
	fmc = FMC(hostname=hostname, username=username, password=password, domain='Global')
	acPolicies = fmc.policy.accesspolicy.get()

	pol = {}

	print ("ACP available in global domain: ")
	for policy in acPolicies:
		pol[policy['name']] = policy['id']
		print ("\tName: ", policy['name'])

	acp = input("Enter the ACP Name (case sensitive) if you want specific check for specific ACP (multiple values should be comma seperated). By default all the ACP would be checked, press return for default behaviour: ")
	action_on_rule=input(""" 

*********************************

Enter 'delete' to delete Expired rules
Enter 'disable' to disable Expired rules
or Enter anything to continue with just reports:      """)
	action_on_rule=action_on_rule.strip()
	selection = []

	if (acp):
		temp = acp.split(",")
		for local in temp:
			local = local.replace(" ", "")
			selection.append(pol[local])
	else:
		for local in acPolicies:
			selection.append(local['id'])

	objectGuide(fmc)
	acpCSV(fmc, selection,action_on_rule)

def acpCSV(fmc, selection,action_on_rule):
	print ("Inside ACP")
	row=1
	for policy in selection:
		ac_policy = policy
		rules = fmc.policy.accesspolicy.accessrule.get(policy)
		refRules = {}
		pos = 0
		for ele in rules:
			#print("##########################")
			pos = pos + 1
			
			#TimeBased Objects

			if ("timeRangeObjects" in ele.keys()):
				for local in ele['timeRangeObjects']:
					trObj = local['name']
			else:
				trObj = "NULL"

			if (trObj in expired):
				expiredRules[ele['name']] = trObjects[trObj]
				display_output(row,ele['metadata']['accessPolicy']['name'],ele['metadata']['ruleIndex'],ele['name'],trObjects[trObj][0]+" "+trObjects[trObj][1])

				if (action_on_rule == "delete" or action_on_rule =="Delete"):
					fmc.conn._request('delete',ele['links']['self'])

				if (action_on_rule == "disable" or action_on_rule =="Disble"):
					del ele['metadata']
					ele['enabled'] = "False"
					fmc.conn._request('put',ele['links']['self'],data=ele)
				
				print("Successfully Written rule {0} of {1}".format(ele['metadata']['ruleIndex'],ele['metadata']['accessPolicy']['name']))
				
				row=row+1
		

def display_output(row,access_policy_name,id_num,rule_name,Expired_Date):
	worksheet.write(row,0,access_policy_name,style4)
	worksheet.write(row,1,id_num,style4)
	worksheet.write(row,2,rule_name,style4)
	worksheet.write(row,3,Expired_Date,style4)

getInput()
workbook.close() 
