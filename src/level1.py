DATA_TYPES_SUPPORTED=["string","integer","boolean"]

from flask import (Flask, abort, jsonify, Response,render_template)
from flask import request as flask_request

def data_type_error(function_name,variable_name,expected_type_name,input):
	raise Exception("MoRBs:"+str(function_name)+":ERROR: '"+
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
	- request is not the type of flask.request
	- inputs is not a list
	- inputs is not a list of strings
"""


def reciever(request, expected={}, recieve_nothing = False):
	if recieve_nothing == True:
		return nothing_reciever
	
	# Validating that request has the type of flask.request
	validate_expected(expected)

	if type(request) != type(flask_request):
		data_type_error("reciever","request","flask.request",request)
	#Validating that expected is a dict
	# Now we are sure that expected is a list of strings, 
	# and we got rid of all developers errors

	if len(expected)!=0:
		if request.method != "GET":
			return json_reciever(request,expected)		
	return {"success":True,"result":{}}









def nothing_reciever():
	return {"success":True,"result":{}}




def json_reciever(request, expected={}):
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
			It represents whther the function was able to recieve inputs or not
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
	- all is not boolean
	- "expected" is not as expected
	- recieved does not pass (validate_attendance_from_expected)
	- 'old_values' is not None, and it doesn't pass 
		(validate_attendance_from_expected)
"""



#To Be continued
def attendance_validator(expected,recieved,all=True,old_values=None):
	#validating that all has a boolean type
	if type(all)!=bool:
		data_type_error(function_name="attendance_validator",
			variable_name="all",expected_type_name="boolean",imput=all)

	#NOTE: reciever has already filled empty data with "None"
	validate_attendance_from_expected(recieved,"recieved",expected)

	#In this case there are old values
	if old_values!= None:
		validate_attendance_from_expected(old_values,"old_values",expected)

	#validaing that "all" has a type of boolean
	if type(all) != bool:
		data_type_error(function_name="attendance_validator",
			variable_name="all",expected_type_name="boolean",imput=all)
	#To Be continued
	
















"""
new_attendance_validator

- INPUTS:
	- expected: the dictiony of the expected data and how they look like 
		-Example: {"name":"string","price":"integer","in_stock":"boolean"}
	- recieved_result: the dictionary of the recieved result (recieved["result"])
- FUNCTION:
	- it will raise error if the recieved_result is not validated
	- it will tell wehther there has been any inputs missing in the request
- OUTPUTS:
	- a dictionary with these values {"success": ... , "result": ... }
		- "success": a boolean: True or False
			It represents whther the function was able to recieve inputs or not
		- "result":
			- if success == True: a dictionary of the expected variables
				Without any None at all, and at the same expected formatting
				Example: {"a":1, "b":2, "c":"5"}
				None: there will be nothing called None here
			- if success == False: dictionry of "status" code of failure and reason
				Example: {"status":400,"desctiption":"a is missing"}
NOTES:
	- expected is not a user input, it is a developer creation,
		that is why it raises error, not validate with success or failure

ERROR:
	- recieved result failed to pass validate_attendance_from_expected
	- a value in the recieved_result is equal to None
"""
def new_attendance_validator(expected,recieved_result):
	#NOTE: reciever has already filled empty data with "None"
	validate_attendance_from_expected(recieved_result,"recieved",expected)
	
	#Now we are sure that we have all values
	#We need to make sure that there are no valuesa that have the value of None
	#Bacause it is a post method
	#and we can not allow empty fields
	#empty fields are user mistake, not developer's mistakes
	# they will not raise error, rather they will just fail
	toReturn = {}
	for key in expected:
		toReturn[key] = recieved_result[key]
		if recieved_result[key] == None:
			return {"success":False,"result":{"status":400, 
			"description":str(key) +" is missing"}}

	return {"success":True,"result":toReturn}







def old_attendance_validator(expected,recieved_result,old_dict):
	#NOTE: reciever has already filled empty data with "None"
	validate_attendance_from_expected(recieved_result,"recieved",expected)
	validate_attendance_from_expected(old_dict,"old_dict",expected)
	
	#Now we are sure that we have all values
	#We need to make sure that there are no valuesa that have the value of None
	#Bacause it is a post method
	#and we can not allow empty fields
	#empty fields are user mistake, not developer's mistakes
	# they will not raise error, rather they will just fail
	toReturn = {}
	for key in expected:
		toReturn[key] = recieved_result[key]
		if recieved_result[key] == None:
			return {"success":False,"result":{"status":400, 
			"description":str(key) +" is missing"}}

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
		reciever, it is a developer creation,
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
		-Example: "expected" or "recieved"
- FUNCTION:
	- we need to make sure this is a dictionary
	- we need to make sure that input_dict does not have any value of None
- OUTPUTS:
	- no outputs, errors are raised if somethng went wrong

NOTES:
	- input_dict is not a user input, it is supposed to be a complete dict
		reciever, it is a developer creation,
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



