from flask import (Flask, 
	request, abort, jsonify, Response,render_template)
"""
reciever:

INPUTS:
	- request: the request variable
	- inputs: a list of strings containing the names of the predicted
	 	variables passed in the request body
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


def reciever(request, inputs):
	toReturn = {}
	#vValidating that input_request has the type of flask.request
	if type(input_request) != type(request):
		raise Exception("MORG:reciever:ERROR: 'input_request' is supposed to be have "+
			"the type of flask.request, but found type of "+ 
			str(type(input_request)))
	#Validating that inputs is a list
	if type(inputs) != type([]):
		raise Exception("MORG:reciever:ERROR:"+
			" The 'inputs'' varbiale has a type of " + str(type(inputs)) +
			", type of 'inputs' is supposed to be 'list'.")
	#Validating that inputs is a list of strings
	for inputs_index in inputs:
		if type(inputs[inputs_index]) != str:
			raise Exception("MOAG:reciever:ERROR:"+
			" The 'inputs'' varbiale is supposed to be a list of strings, " + 
			"one of the elements was found to be "+str(type(inputs[inputs_index])))
	#Validating that the request can be parsed to JSON
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
	for inputs_index in inputs:
		toReturn[inputs[inputs_index]] = body.get(inputs[inputs_index],None)
	return {"success":True,"result":toReturn}
