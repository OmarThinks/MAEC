def reciever(request, inputs):
	toReturn = {}
	if type(inputs) != type([]):
		raise("MOAG:reciever:ERROR:"+
			" The 'inputs'' varbiale has a type of " + str(type(inputs)) +
			", type of 'inputs' is supposed to be 'list'.")
	for inputs_index in inputs:
		if type(inputs[inputs_index]) != str:
			raise("MOAG:reciever:ERROR:"+
			" The 'inputs'' varbiale is supposed to be a list of strings, " + 
			"one of the elements was found to be "+str(type(inputs[inputs_index])))
	try:
		body = request.get_json()
	except:
		return {"success":False,"result":{"status":400, 
			"description":"request body can not be parsed to json"}}
	try:
		for inputs_index in inputs:
			toReturn[inputs[inputs_index]] = body.get(inputs[inputs_index],None)
	except:
		return {"success":False,"result":{"status":400, 
			"description":"there is no request body"}}
	retrun {"success":True,"result":toReturn}
