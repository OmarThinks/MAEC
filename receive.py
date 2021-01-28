"""
json_receiver

Inputs:
	- request: the Flask request
	- saModel: the SQLAlchemy model
	- neglect: list of the names of the fields to be neglected
		- Example : ["id","in_stock"]
	- extra: things to expect that are not in the samodel columns
		- Example ["page","max_in_page"]
- Function: 
	- Convert what has been sent to 2 separate groups,
		or readering what has benn sent sa a JSON request
- Output:
	- a dictionary of the fields that has been sent, 
	and whether they have been sent or not
	- Example 
	{
		"result":
		{	"name":1,"price":50.1, 
			"in_stock":None, "amount": NotReceived()
		}
		"extra":
		{
			"page":NoReceived(),
			"maximum_in_page": 40
		}
	}
- Note:
	- NotReceived() is an object, which is not equal to None
		- NotRecieved() :means that has not been sent at all
		- None :it was sent with the value of None
"""
from classes.errors import *
from classes.classreader import filteredSaModelColumnsNames

def json_receiver(request, saModel, neglect=None, extra=None):
#def json_receiver(request, expected={}):
	validate_fields(function_name="json_receiver",variable_name="neglect",
			fields=neglect)
	validate_fields(function_name="json_receiver",variable_name="extra",
			fields=extra)


	
	result={}
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
	
	# what are the values that are required
	to_expect=filteredSaModelColumnsNames(saModel,neglect)

	result = {}
	#receiving data
	for key in to_expect:
		result[key] = body.get(key,None)
	
	#receiving data
	extra_values = {}
	if extra!=None:
		for key in extra:
			extra_results[key] = body.get(key,None)
	return {"success":True,"result":result,"extra_results":extra_results}








