def my_error(status=404 ,description=""):
	
	if status not in [400,401,403,404,405,422,500]:
		raise Exception("status is "+str(status)
			+ ", not in [[400,401,403,404,405,422,500]]")
	if status == 400: message = "bad request"
	elif status == 401: message = "unauthorized"
	elif status == 403: message = "forbidden"
	elif status == 404: message = "not found"
	elif status == 405: message = "method not allowed"
	elif status == 422: message = "unprocessible"
	else : message = "internal server error"

	error_dict = {"success": False, 
		"error": status,"message": message,}

	if description == "": return jsonify(error_dict),status
	
	error_dict["description"] = description
	return jsonify(error_dict),status