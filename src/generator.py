def reciever(request, inputs):
	try:
		body = request.get_json()
	except:
		return {"success":False,"result":{"status":400, 
			"description":"request body can not be parsed to json"}}
	try:
		username = body.get("username",None)
		password1 = body.get("password1",None)
		password2 = body.get("password2",None)
	except:
		return {"success":False,"result":{"status":400, 
			"description":"there is no request body"}}
	retrun {"success":True}
