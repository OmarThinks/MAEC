from flask import Flask, jsonify, request
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import Column, Integer, String, Boolean, Float


import sys
sys.path.insert(0,'..')
from classes.classreader import convert_class_to_dict
from receive import json_receiver


engine = create_engine('sqlite:///database/database.sqlite', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()


class Product(Base):
	__tablename__ = 'products'
	id = Column(Integer, primary_key=True)
	name = Column(String)
	price = Column(Float)
	in_stock = Column(Boolean)

Base.query = db_session.query_property()
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

def create_app():

	app = Flask(__name__)
	app.debug = True
		
	@app.route("/")
	def home_route():
		return jsonify({"type(Product)":str(type(Product)),
			"type(Product.id)":str(type(Product.id))}),200








	@app.route("/receiver/1", methods=["POST"])
	def receiver_test_case1():
		# request is not request type
		try:
			json_receiver(request=1, saModel = 1, neglect=None, extra=None)
		except Exception as e:
			return jsonify({"message":str(e)}),200

	@app.route("/receiver/2", methods=["POST"])
	def receiver_test_case2():
		# saModel fails
		try:
			json_receiver(request=request, 
				saModel = 1, neglect=None, extra=None)
			return jsonify({"message":"abc"}),200
		except Exception as e:
			return jsonify({"message":str(e)}),200


	@app.route("/receiver/3", methods=["POST"])
	def receiver_test_case3():
		# neglect fails
		try:
			json_receiver(request=request, 
				saModel = Product, neglect=["abc","dfg",123], 
				extra=None)
			return jsonify({"message":"abc"}),200
		except Exception as e:
			return jsonify({"message":str(e)}),200

	@app.route("/receiver/4", methods=["POST"])
	def receiver_test_case4():
		# extra fails
		try:
			json_receiver(request=request, 
				saModel = Product, neglect=["abc","dfg","789"], 
				extra=["abc","123",123])
			return jsonify({"message":"abc"}),200
		except Exception as e:
			return jsonify({"message":str(e)}),200

	@app.route("/receiver/5", methods=["POST"])
	def receiver_test_case4():
		# neglect fails, a field is not in the asModel
		try:
			json_receiver(request=request, 
				saModel = Product, neglect=["abc"], 
				extra=None)#'abc' is not a field in the saModel
			return jsonify({"message":"abc"}),200
		except Exception as e:
			return jsonify({"message":str(e)}),200




	@app.route("/receiver_test/<int:test_case_id>", methods=["POST"])
	def receiver_test(test_case_id):
		"""
		This endpont is created to test the receiver endpoint
		it will return the same exact return value of the receiver function
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
		expected ={}
		if test_case_id == 1: #This is successful
			expected = {"name":"string","price":"string","in_stock":"string"}
			#This is successful
		if test_case_id == 2: #This is successful
			expected = {}
			#This is successful
		if test_case_id == 3: #This is the first error
			my_request = 1
			#Fail: request should be of type flask.request
		if test_case_id == 4: #This is the first error
			my_request = 1
			expected = {"name":"string","price":"string","in_stock":"string"}
			#Fail: request should be of type flask.request
		if test_case_id==5: 
			#This is second error
			expected = "This will fail"
			#Fail: expected should be a list of strings, not a string
		if test_case_id == 6: #This is the third error (Example:1)
			expected = ["a","b",["1","2"]]
			#Fail: There can not be an array inside an array
		if test_case_id == 7: #This is the third error (Example:2)
			expected = ["1","c",3]
			#Fail: Only stirngs are allowed
		if test_case_id == 8: #This is the third error (Example:2)
			expected = {"name":"string","price":"string","in_stock":"string"}
			return receiver(request= my_request,
				expected=expected,receive_nothing=True)
			#Fail: Only stirngs are allowed
		try:
			result = receiver(request= my_request,expected=expected)
			if result["success"]==True:
				return jsonify(result)
			else:
				return my_error(fullError=result["result"])
		except Exception as e:
			#raise e#print(str(e))
			return my_error(fullError={"status":500,"description":str(e)})

	return app











if __name__ == "__main__":
	create_app().run()