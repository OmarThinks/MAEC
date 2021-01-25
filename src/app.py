TESTING=True
"""
IMORTANT:
TESTING=False 	IN CASE OF PRODUCTION
TESTING=True 	IN CASE OF TESTING
"""

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
SECRET = "abc"
DATA_TYPES_SUPPORTED=["string","integer","boolean","float"]

from validation import *
from error import *
from level1 import *
from objects import *



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
	print(convert_class_to_dict(sample,case = "all"))
	print(sample.metadata)
	try:
		db.create_all()
	except:
		pass
	#populate_tables()
	print(convert_class_to_dict(sample,case = "all"))
	print(sample.metadata)

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