TESTING=True
"""
IMORTANT:
TESTING=False 	IN CASE OF PRODUCTION
TESTING=True 	IN CASE OF TESTING
"""
import os
import string
import secrets
from flask import (Flask, 
	request, abort, jsonify, Response,render_template)
from flask_cors import CORS
from flask_migrate import Migrate 
from flask_sqlalchemy import SQLAlchemy
from random import shuffle
import json
from random import shuffle

try:
	from __init__ import *
except:
	from src import *






"""
try:
	from .auth import *
	from .models import *
	from .functions import *
except:
	from __init__ import *
	from auth import *
	from models import *
	from functions import *
"""



#SECRET=secrets.token_urlsafe(4)
#SECRET="abc"
#print(SECRET,flush=True)
#SECRET="ABCDEFGHIGKJKFDTGAYAJHGJHSAYTF"
"""
endpoints:
	1)	"/clear_tables"-------->"GET" , "OPTIONS"
	2)	"/populate" ->--------->"GET" , "OPTIONS"
	3)	"/user"		----------->"POST", "DELETE"
	3)	"/products"	->--------->"GET" , "POST" , "OPTIONS"
	4)	"/products/product_id"->"DELETE" , "PUT" , "OPTIONS"
	5)	"/orders"	->--------->"GET" , "POST" , "OPTIONS"
	6)	"/orders/product_id"--->"DELETE" , "PUT" , "OPTIONS"

"""


class config_test:
	#SECRET_KEY=os.urandom(32)
	SECRET_KEY=secrets.token_urlsafe(5000)
	basedir = os.path.abspath(os.path.dirname(__file__))
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = "sqlite:///{}".format(
		os.path.join(os.path.dirname(os.path.abspath(__file__)), 
			"testing_databases/test.sqlite"))
	SQLALCHEMY_TRACK_MODIFICATIONS= False


def create_app(DOCKER=False,testing=TESTING):
	# create and configure the app
	app = Flask(__name__)
	#db=SQLAlchemy(app)
	app.config.from_object(config_test)
	db.app = app
	migrate = Migrate(app,db)
	db.init_app(app)
	try:
		db.create_all()
	except:
		pass
	#populate_tables()
	

	CORS(app,resources={r"*":{"origins":"*"}})
	@app.after_request
	def after_request(response):
		response.headers.add("Access-Control-allow-Origin","*")
		response.headers.add("Access-Control-allow-Headers",
			"Content-Type,Autorization,true")
		response.headers.add("Access-Control-allow-Methods",
			"GET,PUT,POST,DELETE,OPTIONS")

		db.session.rollback()
		#print("roll back", flush=True)
		return response
		


	"""
	1)	"/clear_tables"-------->"GET" , "OPTIONS"
	"""
	@app.route("/clear_tables", methods=["GET"])
	def clear_all_tables():
		test_only()
		db_drop_and_create_all()
		"""
Tests: test_02_populate_test
		"""
		return jsonify({"success":True})









	@app.route("/reciever_test/<int:test_case_id>", methods=["POST"])
	def reciever_test(test_case_id):
		"""
		This endpont is created to test the reciever endpoint
		it will return the same exact return value of the reciever function
		"""
		"""try:
			my_request = request
		except:
			print("NO",flush=True)"""

		"""try:
			username = body.get("username",None)
			password1 = body.get("password1",None)
			password2 = body.get("password2",None)
		except:
			return my_error(status=400, 
				description = "there is no request body")"""
		my_request = request
		inputs = []
		if test_case_id == 1: #This is the first error
			my_request = 1
			#Fail: request should be of type flask.request
		if test_case_id==2: 
			#This is second error
			inputs = "This will fail"
			#Fail: inputs should be a list of strings, not a string
		if test_case_id == 3: #This is the third error (Example:1)
			inputs = ["a","b",["1","2"]]
			#Fail: There can not be an array inside an array
		if test_case_id == 4: #This is the third error (Example:2)
			inputs = ["1","c",3]
			#Fail: Only stirngs are allowed
		if test_case_id == 0: #This is successful
			inputs = ["name","price","in_stock"]
			#This is successful
		#print(my_request,flush=True)
		try:
			result = reciever(request= my_request,inputs=inputs)
			if result["success"]==True:
				return jsonify(result["result"])
			else:
				return my_error(fullError=result["result"])
		except Exception as e:
			#raise e
			return my_error(fullError={"status":500,"description":str(e)})

































	"""
	2)	"/populate" ->--------->"GET" , "OPTIONS"
	"""
	@app.route("/populate", methods=["GET"])
	def populate_all_tables():
		test_only()
		#This endpoint will clear all the data in the database and 
		#populate with new data
		try:
			populate_tables()
			return jsonify({"success":True})
		except:
			abort(422) #Unprocessible
		"""
Tests: test_01_clear_tables
		"""

























		


	"""
	3)	and 4) Product endpoints
	"""
	@app.route("/products", methods=["GET"])
	def get_products():
		#print("Cookies: "+str(request.cookies),flush=True)
	#This endpoint will return all the products		
		#recievng inputs:
		#in_stock has a fall back value of True (The default)
		in_stock = request.args.get('in_stock',True)

		#in stock now has one of two values
		#1) input value
		#2) True (Fall back value)
		#-	I can not be equal to None at all
		#-	Even if equal to None, it will be rejected
		in_stock_validation = validate_must(
			input=in_stock,type="b",input_name_string="in_stock")

		#Now we will validate the in_stock input
		if in_stock_validation["case"] == True:
			# Success: True or false
			in_stock=in_stock_validation["result"]		
		else:
			# Failure: Can't convert to boolean or None (Impossible)
			return in_stock_validation["result"]

		#Now: There are 2 possibilties
			#1) in_stock = True
			#2) in_stock=False
			#input now must have been converted to True or False

		if in_stock == True:
			products = get_in_stock_products()
		else:
			products = Product.query.order_by(Product.id).all()
		
		to_return=[p.simple() for p in products]
		return jsonify({"success":True,"products":to_return})
		

	@app.route("/products", methods=["POST"])
	#@requires_auth()
	def post_products(payload):
	#This endpoint will add a new product
		#print(payload,flush=True)
		try:
			body = request.get_json()
		except:
			return my_error(status=400,
				description="request body can not be parsed to json")
		try:
			name = body.get("name",None)
			price = body.get("price",None)
			in_stock = body.get("in_stock",None)
			#seller_id = body.get("seller_id",None)
		except:
			return my_error(status=400, 
				description = "there is no request body")

		#Validating inputs one by one
		name_validation = validate_must(
			input=name,type="s",input_name_string="name",
			minimum=3,maximum=150)
		price_validation = validate_must(
			input=price,type="f",input_name_string="price",
			minimum=0.1,maximum=1000000)
		in_stock_validation = validate_must(
			input=in_stock,type="b",input_name_string="in_stock")
		#seller_id_validation = validate_must(
		#	input=seller_id,type="i",input_name_string="seller_id",
		#	minimum=1,maximum=100000000000000000)

		#Validating inputs a group
		val_group=validate_must_group(
			[name_validation,price_validation,
			in_stock_validation])

		#Now we will validate all inputs as a group
		if val_group["case"] == True:
			# Success: they pass the conditions
			name,price,in_stock=val_group["result"]		
		else:
			# Failure: Something went wrong
			return val_group["result"]

		seller_id = payload["uid"]
		users_query=User.query
		user_id_validation=validate_model_id(
			input_id=seller_id,model_query=users_query
			,model_name_string="user")
		if user_id_validation["case"]==1:
			#The user exists
			seller=user_id_validation["result"]
		else:
			#No user with this id, can not convert to int,
			# or id is missing
			return my_error(
				status=user_id_validation["result"]["status"],
				description=user_id_validation
				["result"]["description"])		 
		seller_id = seller.id

		#Create the product
		new_product = Product(name=name, price=price,
			seller_id=seller_id, in_stock=in_stock)

		#Insert the product in the database
		try:
			new_product.insert()
			return jsonify(
				{"success":True,"product":new_product.simple()})
		except Exception as e:
			db.session.rollback()
			abort(500)


		


	@app.route("/products/<int:product_id>", methods=["PUT"])
	#@requires_auth()
	def edit_products(payload,product_id):
	#This endpoint will add a new product
	#This is the correct arrangement
	#payload then product id
	#the opposite will result in error
		#print("product_id: "+str(product_id),flush=True)
		#print("payload: "+str(payload),flush=True)
		try:
			body = request.get_json()
		except:
			return my_error(status=400,
				description="request body can not be parsed to json")
		try:
			name = body.get("name",None)
			price = body.get("price",None)
			in_stock = body.get("in_stock",None)
		except:
			return my_error(status=400, 
				description = "there is no request body")
		
		#There can not be 0 fields to change
		#There must be at least one input field
		if (name==None and price==None and in_stock==None):
			return my_error(status=400, 
				description = "you must at least enter"
				" one field to change")

		products_query=Product.query

		product_id_validation=validate_model_id(
			input_id=product_id,model_query=products_query
			,model_name_string="product")
		if product_id_validation["case"]==1:
			#The product exists
			product=product_id_validation["result"]

		else:
			#No product with this id, can not convert to int,
			# or id is missing (Impossible)
			return my_error(
				status=product_id_validation["result"]["status"],
				description=product_id_validation
				["result"]["description"])
		 
		#Now, we have "product", this is essential

		#there will be no None
		if name == None:name=product.name
		if price == None:price=product.price
		if in_stock == None:in_stock=product.in_stock
		#Now there is no None
		#There are default values
		#This step can not change it's place because
		#here we need default values
		
		name_validation = validate_must(
			input=name,type="s",input_name_string="name",
			minimum=3,maximum=150)
		price_validation = validate_must(
			input=price,type="f",input_name_string="price",
			minimum=0.1,maximum=1000000)
		in_stock_validation = validate_must(
			input=in_stock,type="b",input_name_string="in_stock")
		#seller_id_validation = validate_must(
		#	input=seller_id,type="i",input_name_string="seller_id",
		#	minimum=1,maximum=100000000000000000)
		#seller_id can not change

		val_group=validate_must_group(
			[name_validation,price_validation,
			in_stock_validation])

		#Now we will validate all inputs as a group
		if val_group["case"] == True:
			# Success: they pass the conditions
			name,price,in_stock,=val_group["result"]		
		else:
			# Failure: Something went wrong
			return val_group["result"]

		#Making sure that this user can change this product
		if int(product.seller_id) != payload["uid"]:
			return my_error(
				status=403,
				description=
				"you can not change this product, because"+
				" you are not the one who created it")

		#Finally: applying changes
		product.name=name
		product.price=price
		product.in_stock=in_stock

		try:
			product.update()
			return jsonify(
				{"success":True,"product":product.simple()})
		except Exception as e:
			db.session.rollback()
			abort(500)


		

	@app.route("/products/<int:product_id>", methods=["DELETE"])
	#@requires_auth()
	def delete_products(payload,product_id):
	#This endpoint will delete an existing product
		
		products_query=Product.query
		product_id_validation=validate_model_id(
			input_id=product_id,model_query=products_query
			,model_name_string="product")
		if product_id_validation["case"]==1:
			#The product exists
			product=product_id_validation["result"]

		else:
			#No product with this id, can not convert to int,
			# or id is missing (Impossible)
			return my_error(
				status=product_id_validation["result"]["status"],
				description=product_id_validation
				["result"]["description"])
		 
		#Now, we have "product", this is essential

		#Making sure that this user can delete this product
		if int(product.seller_id) != payload["uid"]:
			return my_error(
				status=403,
				description=
				"you can not delete this product, because"+
				" you are not the one who created it")

		try:
			# Finally, deleting the product itself
			product.delete()
			return jsonify(
				{"success":True,
				"result":"product deleted successfully"})
		except Exception as e:
			db.session.rollback()
			abort(500)


	@app.route("/products/users", methods=["GET"])
	#@requires_auth()
	def get_products_users(payload):
		user_id=int(payload["uid"])
		products = Product.query.filter(
			Product.seller_id==user_id).order_by(
			Product.id).all()
		to_return=[p.simple() for p in products]
		return jsonify({"success":True,"products":to_return})


































	def return_error(id):
		if id==1:
			return jsonify({"success":False,"error":400,
			"message":"bad request",
			"details":"missing request body"
			}),400
		if id==2:
			return jsonify({"success":False,"error":400,
			"message":"bad request",
			"details":"missing required variables in request body"
			}),400
		if id==3:
			return jsonify({"success":False,"error":422,
			"message":"unprocessible",
			"details":"there is a mistake in data types"
			}),422
		if id==4:
			return jsonify({"success":False,"error":422,
			"message":"unprocessible",
			"details":"this category id is not in the database"
			}),422			

		if id==5:
			return jsonify({"success":False,"error":422,
			"message":"unprocessible",
			"details":"this question id is not in the database"
			}),422			



	




	@app.errorhandler(400)
	def bad_request(error):
		return jsonify({"success":False,"error":400,
			"message":"bad request"}),400


	@app.errorhandler(401)
	def unauthorized(error):
		return jsonify({"success":False,"error":401,
			"message":"unauthorized"}),401


	@app.errorhandler(403)
	def forbidden(error):
		return jsonify({"success":False,"error":403,
			"message":"forbidden"}),403


	@app.errorhandler(404)
	def not_found(error):
		return jsonify({"success":False,"error":404,
			"message":"not found"}),404


	@app.errorhandler(405)
	def method_not_allowed(error):
		return jsonify({"success":False,"error":405,
			"message":"method not allowed"}),405


	@app.errorhandler(422)
	def unprocessible(error):
		return jsonify({"success":False,"error":422,
			"message":"unprocessible"}),422


	@app.errorhandler(500)
	def internal_server_error(error):
		return jsonify({"success":False,"error":500,
			"message":"internal server error"}),500



	def test_only():
		if testing == False:
			abort(404)

	
	return app	

if __name__ == '__main__':
	create_app().run()