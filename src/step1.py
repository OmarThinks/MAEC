#Step1: recieve all the inputs







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





