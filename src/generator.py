DATA_TYPES_SUPPORTED=["string","integer","boolean"]

from flask import (Flask, 
	request, abort, jsonify, Response,render_template)


def data_type_error(function_name,variable_name,expected_type_name,input):
	raise Exception("MoRG:"+str(function_name)+":ERROR: '"+
		str(variable_name)+"' is supposed to have "+
		"the type of '"+str(expected_type_name)+"', but found type of '"+ 
		str(type(input))+"' instead")




"""
reciever:

INPUTS:
	- request: the request variable
	- inputs (Optional): a list of strings containing the names of the predicted
	 	variables passed in the request body
	 	In case of not entring the inputs value, it has a defualt value of []
	 	and the return value will be {}
FUNCTION:
	- This function recievs the inputs of the endpoint, that are as a JSON request body
OUTPUTS:
	- a dictionary with these values {"success": ... , "result": ... }
		- "success": a boolean: True or False
			It represents whther the function was able to receve inputs or not
		- "result":
			- if success == True: a dictionary of the expected variables
				Example: {"a":1, "b":2, "c":None}
				None:means that this varaiable was not recieved successfully
			- if success == False: dictionry of "status" code of failure and reason
				Example: {"status":400,"description":"there is no request body"}
- Example:
	Please check the file "test_app.py" to see how it works
	there is an endpoint called "reciever_test"

ERRORS:
	- input_request is not the type of flask.request
	- inputs is not a list
	- inputs is not a list of strings
"""


def reciever(input_request, expected={}):
	toReturn = {}
	# Validating that request has the type of flask.request

	validate_dict(expected,"reciever","expected",full=True)

	if type(input_request) != type(request):
		data_type_error("reciever","input_request","flask.request",input_request)
	#Validating that expected is a dict
	# Now we are sure that expected is a list of strings, 
	# and we got rid of all developers errors

	if len(expected)!=0:
		#Validating that the input_request can be parsed to JSON
		try:
			body = input_request.get_json()
		except:
			return {"success":False,"result":{"status":400, 
				"description":"request body can not be parsed to json"}}
		#Validating that there is a request body
		try:
			testing = body.get("testing",None)
		except:
			return {"success":False,"result":{"status":400, 
				"description":"there is no request body"}}
		#Finally, return values
		for key in (expected):
			toReturn[key] = body.get(expected[key],None)
	else:
		toReturn={}
	return {"success":True,"result":toReturn}


















"""
attendance_validator:

INPUTS:
	- expected: a dictionary that represent what is expected
		- Example: {"name":"string", "price": "integer", "in_stock":"boolean"}
	- recieved: a dictionary of recieved values
		- Example: {"name":"abc","price":5,"in_stock":True}
		- Example: {"name":None,"price":5,"in_stock":True}
		- Example: {"name":None,"price":None,"in_stock":None}
		- Example: {}
	- all: a boolean value
		- represents whther or not all values are required
		- True: all values are required
			If one value is missing, it will fail
		- False: at least one value is required
			if all are equal to None. or they do not exist, it will fail
	- old_values: If all==False, then old values must be entered
		- old_values is a dict containing the old values before replacement
		- It must have the same keys as the keys of expected

FUNCTION:
	- This function handels the recieved inputs
	- And make sure that they are as expected, all attending
OUTPUTS:
	- a dictionary with these values {"success": ... , "result": ... }
		- "success": a boolean: True or False
			It represents whther the function was able to receve inputs or not
		- "result":
			- if success == True: a dictionary of the expected variables
				Without any None at all, and at the same expected formatting
				Example: {"a":1, "b":2, "c":"5"}
				None: there will be nothing called None here
			- if success == False: dictionry of "status" code of failure and reason
				Example: {"status":400,"desctiption":"a is missing"}
- Example:
	Please check the file "test_app.py" to see how it works
	there is an endpoint called "reciever_test"

ERRORS:
	- input_request is not the type of flask.request
	- inputs is not a list
	- inputs is not a list of strings
"""
def attendance_validator(expected,recieved,all=True,old_values=None):
	# Validating that "expected", "recieved" and "old_values" are dicts
	validate_dict(expected,"attendance_validator","expected",full=True)
	validate_dict(old_values,"attendance_validator","old_values",full=False)
	validate_dict(recieved,"attendance_validator","old_values",full=False)
	
	if type(recieved) != dict:
		raise Exception("MORG:attendance_validator:ERROR:"+
			" The 'recieved' varbiale has a type of " + str(type(recieved)) +
			", type of 'recieved' is supposed to be 'dict'.")
	if type(old_values) != dict:
		raise Exception("MORG:attendance_validator:ERROR:"+
			" The 'old_values' varbiale has a type of " + str(type(old_values)) +
			", type of 'old_values' is supposed to be 'dict'.")
	
	#validaing that "all" has a type of boolean
	if type(all) != bool:
		raise Exception("MORG:attendance_validator:ERROR:"+
			" The 'all' varbiale has a type of " + str(type(all)) +
			", type of 'all' is supposed to be 'dict'.")
	
	#validating data types inside the dicts
























def validate_dict(input_dict,function_name,dict_name,full=True):
	if type(input_dict) != dict:
		data_type_error(function_name,dict_name,"dict",input_dict)
	for key in input_dict:
		value = input_dict[key]
		if type(value) != str:
			data_type_error("validate_expected",
				"each element of "+str(function_name),"string",value)
		if not full:
			if value == None:
				continue
		if value not in DATA_TYPES_SUPPORTED:
			raise Exception(
			"MoRG:validate_expected:ERROR: "+
				str(value)+ " is not a supported data type by MoRG")


