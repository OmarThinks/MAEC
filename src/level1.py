from flask import (Flask, abort, jsonify, Response,render_template)
from flask import request as flask_request

try:
	from __init__ import *
except:
	from src import *




"""
receiver:

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
				None:means that this varaiable was not received successfully
			- if success == False: dictionry of "status" code of failure and reason
				Example: {"status":400,"description":"there is no request body"}
- Example:
	Please check the file "test_app.py" to see how it works
	there is an endpoint called "receiver_test"

ERRORS:
	- request is not the type of flask.request
	- inputs is not a list
	- inputs is not a list of strings
"""


def receiver(request, expected={}, receive_nothing = False):
	if receive_nothing == True:
		return nothing_receiver()
	
	# Validating that request has the type of flask.request
	validate_expected(expected)

	if type(request) != type(flask_request):
		data_type_error("receiver","request","flask.request",request)
	#Validating that expected is a dict
	# Now we are sure that expected is a list of strings, 
	# and we got rid of all developers errors

	if len(expected)!=0:
		if request.method != "GET":
			return json_receiver(request,expected)		
	return {"success":True,"result":{}}









def nothing_receiver():
	return {"success":True,"result":{}}




def json_receiver(request, expected={}):
	toReturn={}
	#Validating that the request can be parsed to JSON
	try:
		body = request.get_json()
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
		toReturn[key] = body.get(key,None)
	return {"success":True,"result":toReturn}













"""
attendance_validator:

INPUTS:
	- expected: a dictionary that represent what is expected
		- Example: {"name":"string", "price": "integer", "in_stock":"boolean"}
	- received: a dictionary of received values
		- Example: {"success":True,"result":{"name":"abc","price":5,"in_stock":True}}
		- Example: {"success":True,"result":{"name":None,"price":5,"in_stock":True}}
		- Example: {"success":True,"result":{"name":None,
				"price":None,"in_stock":None}}
		- Example: {"sucess":True,"result":{}}
		- Example: {"sucess":False,"result":{"status":400,"description":"there"}}
	- old_values: = None (default)
		- it should be a dict containing old values
		- it can not contain None
		- It must have the same keys as the keys of expected
		-Example:
			- {"name":"abc","price":12,"in_stock":True}
			- {}

FUNCTION:
	- This function handels the received inputs
	- And make sure that they are as expected, all attending
	- If there was a value missing in receuved, and it was expected, and it is old
		then it will be filled from old
OUTPUTS:
	- a dictionary with these values {"success": ... , "result": ... }
		- "success": a boolean: True or False
			It represents whether the function was able to receive inputs or not
		- "result":
			- if success == True: a dictionary of the expected variables
				Without any None at all, and at the same expected formatting
				Example: {"a":1, "b":2, "c":"5"}
				None: there will be nothing called None here
			- if success == False: dictionry of "status" code of failure and reason
				Example: {"status":400,"description":"a is missing"}
- Example:
	- {"success":True,"result":{"name":"product","price":5,"in_stock":True}}

ERRORS:
	- "expected" is not as expected
	- new_attendance_validator errors
	- old_attendance_validator errors
"""



def attendance_validator(expected,received,old=None):
	morbs_checkpoint(input_dict=received,
		function_name="attendance_validator",variable_name="received")
	if type(received)!=dict:
		data_type_error(function_name="attendance_validator",
			variable_name="received",expected_type_name="dict",
			input=received)
	#The previous step has failed
	if received["success"] ==  False:
		return received
	toReturn={}
	if old == None:
		#It is a new record, like POST method
		toReturn = new_attendance_validator(expected,
			received_result=received["result"])
	else:
		#the record already exists, like PATCH or PUT methods
		toReturn = old_attendance_validator(expected=expected,
		received_result=received["result"],old_dict=old)
	morbs_checkpoint(input_dict=toReturn,
		function_name="attendance_validator",variable_name="toReturn")
	return toReturn

	 






"""
data_types_validator
"""
def data_types_validator():
	return True

	 













"""
new_attendance_validator

- INPUTS:
	- expected: the dictiony of the expected data and how they look like 
		-Example: {"name":"string","price":"integer","in_stock":"boolean"}
	- received_result: the dictionary of the received result (received["result"])
- FUNCTION:
	- it will raise error if the received_result is not validated
	- it will tell wehther there has been any inputs missing in the request
- OUTPUTS:
	- a dictionary with these values {"success": ... , "result": ... }
		- "success": a boolean: True or False
			It represents whther the function was able to receive inputs or not
		- "result":
			- if success == True: a dictionary of the expected variables
				Without any None at all, and at the same expected formatting
				Example: {"a":1, "b":2, "c":"5"}
				None: there will be nothing called None here
			- if success == False: dictionry of "status" code of failure and reason
				Example: {"status":400,"description":"a is missing"}
NOTES:
	- expected is not a user input, it is a developer creation,
		that is why it raises error, not validate with success or failure

ERROR:
	- received result failed to pass validate_attendance_from_expected
	- a value in the received_result is equal to None
"""
def new_attendance_validator(expected,received_result):
	#NOTE: receiver has already filled empty data with "None"
	validate_attendance_from_expected(received_result,"received",expected)
	
	#Now we are sure that we have all values
	#We need to make sure that there are no values that have the value of None
	#Bacause it is a post method
	#and we can not allow empty fields
	#empty fields are user mistake, not developer's mistakes
	# they will not raise error, rather they will just fail
	toReturn = {}
	for key in expected:
		toReturn[key] = received_result[key]
		if received_result[key] == None:
			return {"success":False,"result":{"status":400, 
			"description":str(key) +" is missing"}}
	return {"success":True,"result":toReturn}










"""
old_attendance_validator

- INPUTS:
	- expected: the dictiony of the expected data and how they look like 
		-Example: {"name":"string","price":"integer","in_stock":"boolean"}
	- received_result: the dictionary of the received result (received["result"])
	- old_dict: a dictionary that contains the old values
		- Example: {"name":"abc","price":123,"in_stock":"boolean"}
- FUNCTION:
	- it will raise error if the received_result is not validated
	- it will raise error if all inputs are missing
	- if there are any missing values it will fill them from the old
- OUTPUTS:
	- a dictionary with these values {"success": ... , "result": ... }
		- "success": a boolean: True or False
			It represents whther the function was able to receive inputs or not
		- "result":
			- if success == True: a dictionary of the expected variables
				Without any None at all, and at the same expected formatting
				Example: {"a":1, "b":2, "c":"5"}
				None: there will be nothing called None here
			- if success == False: dictionry of "status" code of failure and reason
				Example: {"status":400,"description":
				"you must at least enter one value"}
NOTES:
	- expected is not a user input, it is a developer creation,
		that is why it raises error, not validate with success or failure
ERROR:
	- received result failed to pass validate_attendance_from_expected
	- a value in the received_result is equal to None
	- old is not a ready dict
"""
def old_attendance_validator(expected,received_result,old_dict):
	#NOTE: receiver has already filled empty data with "None"
	validate_attendance_from_expected(received_result,"received",expected)
	validate_attendance_from_expected(old_dict,"old_dict",expected)
	
	validateReadyDict(input_dict=old_dict,dict_name="old_dict")
	
	#Now we are sure that we have all values
	#Now we need to make sure that not all the values are equal to none
	toReturn = {}

	if len(expected) != 0:
		all_Nones = True
		for key in expected:
			toReturn[key] = received_result[key]
			if received_result[key] != None:
				#There is at least one value not equal to None
				all_Nones = False
			else:
				#The value is equal to None
				#It must be substituted
				toReturn[key] = old_dict[key]
		if all_Nones:
			return {"success":False,"result":{"status":400, 
				"description" : "you must at least enter one field to change"}}

	return {"success":True,"result":toReturn}











"""
validate_expected

- INPUTS:
	- expected: the dictiony of the expected data and how they look like 
		-Example: {"name":"string","price":"integer","in_stock":"boolean"}
- FUNCTION:
	- it will raise error if the data is not validated
- OUTPUTS:
	- no outputs, errors are raise uf somethng went wrong

NOTES:
	- expected is not a user input, it is a developer creation,
		that is why it raises error, not validate with success or failure

ERROR:
	- expected is not a dict
	- value corresponding to each key is not a string
	- value corresponding to each key is not is the DATA_TYPES_SUPPORTED
"""

def validate_expected(expected):
	if type(expected) != dict:
		data_type_error("validate_expected","expected","dict",expected)
	for key in expected:
		value = expected[key]
		if type(value) != str:
			data_type_error("validate_expected",
				"each element of expected","string",value)
		if value not in DATA_TYPES_SUPPORTED:
			raise Exception("MoRBs:validate_expected:ERROR: "+value
				+" is not a supported data type")




"""
validate_attendance_from_expected

- INPUTS:
	- input_dict: a dictionary that needs to be validated
		- Example: {"name":1, "price":"a", "in_stock": 5}
		- Example: {"name":"1", "price":4}
	- expected: the dictiony of the expected daya and how they look like 
		-Example: {"name":"string","price":"integer","in_stock":"boolean"}
- FUNCTION:
	- we need to make sure that all the keys in expected exist in this input
- OUTPUTS:
	- no outputs, errors are raised if somethng went wrong

NOTES:
	- input_dict is not a user input, it is supposed to be the output of
		receiver, it is a developer creation,
		that is why it raises error, not validate with success or failure
"""

def validate_attendance_from_expected(input_dict,input_dict_name,expected):
	validate_expected(expected)
	if type(input_dict)!= dict:
		data_type_error("validate_attendance_from_expected",
			"input_dict","dict",input_dict)
	#Now we are very sure that we have 2 dictionaries
	for key in expected:
		if key not in input_dict:
			raise Exception("MoRBs:validate_attendance_from_expected:ERROR:"+
				str(input_dict_name)+" did not carry this key '"+
				str(key)+"', but it exists in 'expected' dict")







"""
validateReadyDict

- INPUTS:
	- input_dict: a dictionary that needs to be validated
		- Example: {"name":1, "price":"a", "in_stock": 5}
		- Example: {"name":"1", "price":None}
	- dict_name: sttring that carries the dict name 
		-Example: "expected" or "received"
- FUNCTION:
	- we need to make sure this is a dictionary
	- we need to make sure that input_dict does not have any value of None
- OUTPUTS:
	- no outputs, errors are raised if somethng went wrong

NOTES:
	- input_dict is not a user input, it is supposed to be a complete dict
		receiver, it is a developer creation,
		that is why it raises error, not validate with success or failure
"""
def validateReadyDict(input_dict,dict_name):
	#validating that input is a dict
	if type(input_dict) != dict:
		data_type_error(function_name="validateReadyDict",
			variable_name=dict_name,expected_type_name="dict",input=input_dict)

	# validating that the input_dict really has no None
	for key in input_dict:
		if input_dict[key] == None:
			raise Exception("MoRBs:validateReadyDict:ERROR:"+str(dict_name)+
				":is supposed to be a dictionary without 'None' values")




def morbs_checkpoint(input_dict,function_name,variable_name):
	if type(input_dict)!= dict:
		data_type_error(function_name=function_name,
			variable_name=variable_name,expected_type_name="dict",input=input_dict)
	if "success" not in input_dict:
		missing_data_error(function_name=function_name,
			variable_name = variable_name+"['success']")
	if type(input_dict["success"])!= bool:
		data_type_error(function_name=function_name,
			variable_name=str(variable_name)+"['success']",
			expected_type_name="bool",input=input_dict["success"])
	
	if "result" not in input_dict:
		missing_data_error(function_name=function_name,
			variable_name = variable_name+"['result']")
	if type(input_dict["result"])!= dict:
		data_type_error(function_name=function_name,
			variable_name=str(variable_name)+"['result']",
			expected_type_name="dict",input=input_dict["result"])

	if input_dict["success"] == False:
		if "status" not in input_dict["result"]:
			missing_data_error(function_name=function_name,
			variable_name = variable_name+"['result']['status']")
		if type(input_dict["result"]['status']) != int:
			data_type_error(function_name=function_name,
				variable_name=str(variable_name)+"['result']['status']",
				expected_type_name="int",input=input_dict["result"]['status'])
		if "description" not in input_dict["result"]:
			missing_data_error(function_name=function_name,
			variable_name = variable_name+"['result']['description']")
		if type(input_dict["result"]['description']) != str:
			data_type_error(function_name=function_name,
				variable_name=str(variable_name)+"['result']['description']",
				expected_type_name="str",input=input_dict["result"]['description'])



"""
Unorganizedly written
"""
"""
def validate__dict(input_dict,function_name,dict_name,full=True):
	if type(input_dict) != dict:
		data_type_error("validate_dict",dict_name,"dict",input_dict)
	for key in input_dict:
		value = input_dict[key]
		if not full:
			if value == None:
				continue
		if type(value) != str:
			data_type_error("validate_dict",
				"each element of "+str(dict_name),"string",value)
		if value not in DATA_TYPES_SUPPORTED:
			raise Exception(
			"MoRBs:validate_dict:ERROR: "+
				str(value)+ " is not a supported data type by MoRBs")

"""



