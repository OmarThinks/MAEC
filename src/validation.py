
try:
	from __init__ import *
except:
	from src import *






import json
from flask import Flask, request, jsonify, abort
import base64






def validate_model_id(input_id,model_query,model_name_string):
	#Validate that model id has a value, not None
	if input_id == None: return {"case":4,"result":{"status":400, 
			"description":model_name_string+
			" is missing"}}
	
	#Validate that model id can be converted to int
	try:
		id = int(input_id)
	except:
		return {"case":3,"result":{"status":400, 
			"description":model_name_string+
			" id can not be converted to integer"}} 
		#[False,my_error(status=400, description=model_name_string+" id can not be converted to integer")]
	
	#Validate that id is not negative or zero
	if id<=0:
		return {"case":3,"result":{"status":422, 
			"description":model_name_string+ 
			" id can not be less than"+
			" or equal to 0"}} 

	try:
		item = model_query.filter_by(id=id).all()
	except Exception as e:
		return {"case":3,"result":{"status":400, 
			"description":model_name_string+
			" id can not be converted to integer"}} 
	if len(item) == 0 :
		return {"case":2,"result":{"status":422, 
			"description":"there is no " +model_name_string+
			" with this id"}} 

	return {"case":1,"result":item[0]}





def validate_string(input_string,string_name,minimum_length=0,
	max_length=1000000):
	#Validate that input has a value, not None
	if input_string == None: return {"case":3,"result":None}
	
	#Validate that input can be converted to string
	try:
		result = str(input_string)
	except:
		return {"case":2,"result":{"status":400, 
			"description":string_name+
			" can not be converted to string"}} 
	
	#Validate that input length is less that 100
	if len(result)>max_length:
		return {"case":2,"result":{"status":422, 
			"description":"maximum "+ string_name
			+" length is "+str(max_length)+" letters"}} 

	if len(result)<minimum_length:
		return {"case":2,"result":{"status":422, 
			"description":"minimum "+ string_name
			+" length is "+str(minimum_length)+" letters"}} 

	return {"case":1,"result":result}







def validate_boolean(input_boolean,input_name_string):
	#Validate that product input_boolean has a value, not None
	if input_boolean == None: return {"case":3,"result":None}
	
	#Validate that input_boolean can be converted to boolean

	found_it=False

	if (input_boolean==True or input_boolean=="true" or
	 input_boolean=="True" or input_boolean==1 or
	  input_boolean=="1"):
		found_it=True
		result=True
	if (input_boolean==False or input_boolean=="false" or
	 input_boolean=="False" or input_boolean==0 or
	  input_boolean=="0"):
		found_it=True
		result=False


	if found_it == True:
		return {"case":1,"result":result}
	return {"case":2,"result":{"status":400, 
			"description":input_name_string+" can not be "+
			"converted to boolean"}} 







def validate_integer(
	input_integer,input_name_string,maximum,minimum):
	#Validate that input has a value, not None
	if input_integer == None: return {"case":3,"result":None}
	
	#Validate that input can be converted to int
	try:
		result = int(input_integer)
	except:
		return {"case":2,"result":{"status":400, 
			"description":input_name_string+
			" can not be converted to integer"}} 
	
	#Validate that input is not less than minimum
	if result<int(minimum):
		return {"case":2,"result":{"status":422, 
			"description":input_name_string+
			" can not be less than "+ str(minimum)}} 

	#Validate that input is not more than maximum
	if result>int(maximum):
		return {"case":2,"result":{"status":422, 
			"description":input_name_string+
			" can not be more than "+ str(maximum)}} 
	return {"case":1,"result":result}



def validate_float(
	input_float,input_name_string,maximum,minimum):
	#Validate that input has a value, not None
	if input_float == None: return {"case":3,"result":None}
	
	#Validate that input can be converted to float
	try:
		result = float(input_float)
	except:
		return {"case":2,"result":{"status":400, 
			"description":input_name_string+
			" can not be converted to float"}} 
	
	#Validate that input is not less than minimum
	if result<float(minimum):
		return {"case":2,"result":{"status":422, 
			"description":input_name_string+
			" can not be less than "+ str(minimum)}} 

	#Validate that input is not more than maximum
	if result>float(maximum):
		return {"case":2,"result":{"status":422, 
			"description":input_name_string+
			" can not be more than "+ str(maximum)}} 
	return {"case":1,"result":result}



def validate_base64(
	input_string,input_name_string,maximum_length,minimum_length):
	#Validate that input has a value, not None
	if input_string == None: return {"case":3,"result":None}

	#Validate that input is string
	if type(input_string)!= str:
		return {"case":2,"result":{"status":400, 
			"description":input_name_string+
			" is not a string"}}
		 
	#Validate that input length is not less than minimum
	if len(input_string)<minimum_length:
		return {"case":2,"result":{"status":422, 
			"description":input_name_string+
			" length can not be less than "+ str(minimum_length)+ " characters"}} 

	#Validate that input length is not more than maximum
	if len(input_string)>maximum_length:
		return {"case":2,"result":{"status":422, 
			"description":input_name_string+
			" length can not be more than "+ str(maximum_length)+ " characters"}} 

	validation = isBase64(input_string)
	if validation == True:
		return {"case":1,"result":input_string}
	else:
		return {"case":2,"result":{"status":422, 
			"description":input_name_string+
			" can not be converted to base64"}} 

def validate_specific(input_value,input_name_string,input_range):
	if input_value == None: return {"case":3,"result":None}
	try:
		for elem in input_range:
			if type(input_value) == type(elem):
				if input_value == elem:
					return {"case":1,"result":input_formatting}
	except Exception as e:
		pass
	return {"case":2,"result":{"status":422, 
			"description":str(input_value)+" is not allowed "+str(input_name_string)}} 
		







"""
type:
	- "s" : String
	- "i" : Integer
	- "f" : Float
	- "b" : Boolean
	- "b64" : base64
	- "spfc": specific

"""
def validate__must(input,type,
	input_name_string,maximum=0,minimum=0,input_range=[]):
	validation=0;
	if type == "s":
		validation= validate_string(
			input_string=input,
			max_length=maximum,string_name=input_name_string,
			minimum_length=minimum)
	elif type == "i":
		validation= validate_integer(
	input_integer=input,input_name_string=input_name_string,
	maximum=maximum,minimum=minimum)
	elif type == "f":
		validation= validate_float(
	input_float=input,input_name_string=input_name_string,
	maximum=maximum,minimum=minimum)
	elif type == "b":
		validation = validate_boolean(input_boolean=input
			,input_name_string=input_name_string)
	elif type == "b64":
		validation = validate_base64(
			input_string=input,input_name_string=input_name_string,
			maximum_length=maximum,minimum_length=minimum)
	elif type == "spfc":
		validation = validate_specific(input_value=input,
			input_name_string=input_name_string,input_range=input_range)
	else:
		raise Exception("validate_must: type is"+str(type)
			+ "and it can not be like this, it should be: "+
			"'s', 'i', 'f', 'b', 'b64' or 'spfc'")
	if validation["case"] == 1:
		# Success: correct data type
		return {"case":True,
		"result": validation["result"]}
	elif validation["case"] == 2:
		# Failure: Can't convert to correct data type
		return {"case":False,
		"result": {"status":validation["result"]["status"],
			"description":validation["result"]["description"]}}
	else:
		# no Input is given, result = None
		return  {"case":False,
		"result": {"status":400,"description":
			input_name_string+" is missing"}}





def validate_must(input,type,
	input_name_string,maximum=0,minimum=0):
	
	validation=validate__must(input=input,type=type,
	input_name_string=input_name_string,
	maximum=maximum,minimum=minimum)

	if validation["case"]:
		return validation
	return  {"case":False,
		"result": my_error(
		status=validation["result"]["status"]
			,description=validation["result"]["description"])}





def validate_must_group(validations_list):
	to_return=[]
	for val in validations_list:
		if val["case"]==True:
			to_return.append(val["result"])
		else: 
			return {"case":False,"result":val["result"]}
	return {"case":True,"result":to_return}  







# pass function will validate whther the input is base 64 or not
# True:base64
# False:Not base64
def isBase64(input_string):
	if type(input_string)!=str:
		return False
	if len(input_string)%4 != 0:
		return False
	for char in input_string:
		base64_list = ["a","b","c","d","e","f","g","h","i","j","k","l","m",
		"n","o","p","q","r","s","t","u","v","w","x","y","z",
		"A","B","C","D","E","F","G","H","I","J","K","L","M",
		"N","O","P","Q","R","S","T","U","V","W","X","Y","Z",
		"1","2","3","4","5","6","7","8","9","0","/","=","+"]
		if char not in base64_list:
			return False
	return True














