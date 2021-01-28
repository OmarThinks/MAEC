import os
import secrets
import unittest
import json
import random
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func 
from flask_cors import CORS
from flask_migrate import Migrate 
import base64



from app import create_app




"""


b:validation Functions


"""

unittest.TestLoader.sortTestMethodsUsing = None

class receiver_TestCase(unittest.TestCase):
	"""This class represents the trivia test case"""

	def setUp(self):
		# create and configure the app
		self.app = create_app() #Flask(__name__)
		self.client = self.app.test_client
		#db.app = self.app
		#db.init_app(self.app)
		#db.create_all()        
		
	
	def tearDown(self):
		"""Executed after reach test"""
		print("_+++++++++++++++++++++++++++++++++_")

	#Note: Tests are run alphapetically
	def test_00000_test(self):
		self.assertEqual(1,1)
		print("Test 0:Hello, Tests!")




	def test_a_0_0_0(self):
		print("Testing json_receiver")

	def test_a_1_1_1_json_receiver_tests(self):
		#Testing the function of route "json_receiver_test/int"
		response = self.client().post("/json_receiver/1")
		#Expected to fail, No request body
		data = json.loads(response.data)
		#print(data)
		self.assertEqual(data,{'message': "MoRBs:json_"+
			"json_receiver:ERROR: 'request' is supposed to "+
			"have the type of 'LocalProxy', but found "+
			"type of '<class 'int'>' instead"})
		self.assertEqual(response.status_code,200)
		print("Test a_1_1_1: json_receiver_tests : request not flask_request")

	def test_a_1_1_2_json_receiver_tests(self):
		#Testing the function of route "json_receiver_test/int"
		response = self.client().post("/json_receiver/2")
		#Expected to fail, No request body
		data = json.loads(response.data)
		#print(data)
		self.assertEqual(data,{'message': "MoRBs:"+
			"json_receiver:ERROR: 'saModel' is supposed"+
			" to have the type of 'DeclarativeMeta', but"+
			" found type of '<class 'int'>' instead"})
		self.assertEqual(response.status_code,200)
		print("Test a_1_1_2: json_receiver_tests : Not saModel")

	def test_a_1_1_3_json_receiver_tests(self):
		#Testing the function of route "json_receiver_test/int"
		response = self.client().post("/json_receiver/3")
		#Expected to fail, No request body
		data = json.loads(response.data)
		#print(data)
		self.assertEqual(data,{'message': "MoRBs:"+
			"json_receiver:ERROR: 'element in neglect"+
			" list' is supposed to have the type of 'str'"+
			", but found type of '<class 'int'>' instead"})
		self.assertEqual(response.status_code,200)
		print("Test a_1_1_3: json_receiver_tests : neglect fails")

	def test_a_1_1_4_json_receiver_tests(self):
		#Testing the function of route "receiver_test/int"
		response = self.client().post("/json_receiver/4")
		#Expected to fail, No request body
		data = json.loads(response.data)
		#print(data)
		self.assertEqual(data,{'message': "MoRBs:"+
			"json_receiver:ERROR: 'element in extra "+
			"list' is supposed to have the type of 'str'"+
			", but found type of '<class 'int'>' instead"})
		self.assertEqual(response.status_code,200)
		print("Test a_1_1_4: json_receiver_tests : extra fails")

	def test_a_1_1_5_json_receiver_tests(self):
		#Testing the function of route "json_receiver_test/int"
		response = self.client().post("/json_receiver/5")
		#Expected to fail, No request body
		data = json.loads(response.data)
		#print(data)
		self.assertEqual(data,{'result': {
			'description': 'there is no request body',
			'status': 400}, 'success': False})
		self.assertEqual(response.status_code,200)
		print("Test a_1_1_5: json_receiver_tests : neglect fails,"+
			" a field not in saModel")









	"""def test_c_1_1_1_receiver_tests(self):
		#Testing the function of route "receiver_test/int"
		response = self.client().post("/receiver/1")
		#Expected to fail, No request body
		data = json.loads(response.data)
		self.assertEqual(data,{'description': 
			'there is no request body', 'error': 400, 'message': 'bad request', 
			'success': False})
		self.assertEqual(response.status_code,400)
		print("Test c_1_1_1: receiver_tests : no request body")

	def test_c_1_1_2_receiver_tests(self):
		#Testing the function of route "receiver_test/int"
		response = self.client().post("/receiver_test/1",json={})
		#Expected to Succeed, Error in the server
		data = json.loads(response.data)
		self.assertEqual(data,{"success":True,"result":
			{'in_stock': None, 'name': None, 'price': None}})
		self.assertEqual(response.status_code,200)
		print("Test c_1_1_2: receiver_tests : request body successful, empty")

	def test_c_1_1_3_receiver_tests(self):
		#Testing the function of route "receiver_test/int"
		response = self.client().post("/receiver_test/1",json=
			{'in_stock': True, 'name': "abc", 'price': 5})
		#Expected to succeed,
		data = json.loads(response.data)
		self.assertEqual(response.status_code,200)
		self.assertEqual(data,{"success":True,"result":
			{'in_stock': True, 'name': "abc", 'price': 5}})
		print("Test c_1_1_3: receiver_tests : request body"+
			" successful, full request body")

	def test_c_1_2_1_receiver_tests(self):
		#Testing the function of route "receiver_test/int"
		response = self.client().post("/receiver_test/2",json=
			{'in_stock': True, 'name': "abc", 'price': 5})
		#Expected to succeed, empty response
		data = json.loads(response.data)
		self.assertEqual(response.status_code,200)
		self.assertEqual(data,{"success":True,"result":{}})
		print("Test c_1_2_1: receiver_tests : request body"+
			" successful, full request body")

	def test_c_1_2_2_receiver_tests(self):
		#Testing the function of route "receiver_test/int"
		response = self.client().post("/receiver_test/2")
		#Expected to succeed, empty response
		data = json.loads(response.data)
		self.assertEqual(response.status_code,200)
		self.assertEqual(data,{"success":True,"result":{}})
		print("Test c_1_2_2: receiver_tests : request body"+
			" successful, empty request body")

	def test_c_1_3_1_receiver_tests(self):
		#Testing the function of route "receiver_test/int"
		response = self.client().post("/receiver_test/3")
		#Expected to fail, request has wrong value
		data = json.loads(response.data)
		self.assertEqual(response.status_code,500)
		self.assertEqual(data,{'description': "MoRBs:receiver:ERROR: "+
			"'request' is supposed to have the type of "+
			"'flask.request', but found type of '<class 'int'>' instead",
			 'error': 500, 'message': 'internal server error', 'success': False})
		print("Test c_1_3_1: wrong request type")

	def test_c_1_3_2_receiver_tests(self):
		#Testing the function of route "receiver_test/int"
		response = self.client().post("/receiver_test/3",json={"price":5})
		#Expected to fail, request has wrong value
		data = json.loads(response.data)
		self.assertEqual(response.status_code,500)
		self.assertEqual(data,{'description': "MoRBs:receiver:ERROR: "+
			"'request' is supposed to have the type of 'flask.request'"+
			", but found type of '<class 'int'>' instead", 
			'error': 500, 'message': 'internal server error', 'success': False})
		print("Test c_1_3_2: wrong request type")

	def test_c_1_4_1_receiver_tests(self):
		#Testing the function of route "receiver_test/int"
		response = self.client().post("/receiver_test/3")
		#Expected to fail, request has wrong value
		data = json.loads(response.data)
		self.assertEqual(response.status_code,500)
		self.assertEqual(data,{'description': "MoRBs:receiver:ERROR: 'request' "+
			"is supposed to have the type of 'flask.request', but found type of "+
			"'<class 'int'>' instead", 'error': 500, 'message': 
			'internal server error', 'success': False})
		print("Test c_1_4_1: wrong request type")

	def test_c_1_4_2_receiver_tests(self):
		#Testing the function of route "receiver_test/int"
		response = self.client().post("/receiver_test/3",json={"price":5})
		#Expected to fail, request has wrong value
		data = json.loads(response.data)
		self.assertEqual(response.status_code,500)
		self.assertEqual(data,{'description': "MoRBs:receiver:ERROR: "+
			"'request' is supposed to have the type of 'flask.request'"+
			", but found type of '<class 'int'>' instead", 'error': 500, 
			'message': 'internal server error', 'success': False})
		print("Test c_1_4_2: wrong request type")

	def test_c_1_5_1_receiver_tests(self):
		#Testing the function of route "receiver_test/int"
		response = self.client().post("/receiver_test/5")
		#Expected to fail, request has wrong value
		data = json.loads(response.data)
		self.assertEqual(response.status_code,500)
		self.assertEqual(data,{'description': "MoRBs:validate_expected:ERROR: "+
			"'expected' is supposed to have the type of 'dict', but found "+
			"type of '<class 'str'>' instead", 'error': 500, 
			'message': 'internal server error', 'success': False})
		print("Test c_1_5_1: wrong inputs type")

	def test_c_1_6_1_receiver_tests(self):
		#Testing the function of route "receiver_test/int"
		response = self.client().post("/receiver_test/6")
		#Expected to fail, request has wrong value
		data = json.loads(response.data)
		self.assertEqual(response.status_code,500)
		self.assertEqual(data,{'description': "MoRBs:validate_expected:ERROR: "+
			"'expected' is supposed to have the type of 'dict', but found type "+
			"of '<class 'list'>' instead", 'error': 500, 
			'message': 'internal server error', 'success': False})
		print("Test c_1_6_1: wrong type in inputs")

	def test_c_1_7_1_receiver_tests(self):
		#Testing the function of route "receiver_test/int"
		response = self.client().post("/receiver_test/7")
		#Expected to fail, request has wrong value
		data = json.loads(response.data)
		self.assertEqual(response.status_code,500)
		self.assertEqual(data,{'description': "MoRBs:validate_expected:ERROR: "+
			"'expected' is supposed to have the type of 'dict', but found "+
			"type of '<class 'list'>' instead", 'error': 500, 
			'message': 'internal server error', 'success': False})
		print("Test c_1_7_1: wrong type in inputs")

	def test_c_1_8_1_receiver_tests(self):
		#Testing the function of route "receiver_test/int"
		response = self.client().post("/receiver_test/8")
		#Expected to fail, request has wrong value
		data = json.loads(response.data)
		self.assertEqual(response.status_code,200)
		self.assertEqual(data,{"result":{}, 'success': True})
		print("Test c_1_8_1: wrong type in inputs")

	def test_c_2_1_attendance_validator(self):
		# Perfect no old
		self.assertEqual(attendance_validator(expected=
			{"name":"string","price":"integer","in_stock":"boolean"}
			,received={"success":True,
			"result":{"name":"abc","price":5,"in_stock":True}}),
			{"success":True,"result":{"name":"abc","price":5,"in_stock":True}})
		# Perfect empty no old
		self.assertEqual(attendance_validator(expected={}
			,received={"success":True,
			"result":{"name":"abc","price":5,"in_stock":True}}),
			{"success":True,"result":{}})
		print("Test c_2_1: attendance_validator")
	
	def test_c_2_2_attendance_validator(self):	
		# perfect with old
		self.assertEqual(attendance_validator(expected=
			{"name":"string","price":"integer","in_stock":"boolean"}
			,received={"success":True,
			"result":{"name":"abc","price":5,"in_stock":True}},
			old={"name":"efg","price":9,"in_stock":False}),
			{"success":True,"result":{"name":"abc","price":5,"in_stock":True}})
		# missing values with old
		self.assertEqual(attendance_validator(expected=
			{"name":"string","price":"integer","in_stock":"boolean"}
			,received={"success":True,
			"result":{"name":None,"price":None,"in_stock":True,"data":False}},
			old={"name":"efg","price":9,"in_stock":False,"rty":"741"}),
			{"success":True,"result":{"name":"efg","price":9,"in_stock":True}})
		# empty with old
		self.assertEqual(attendance_validator(expected=
			{}
			,received={"success":True,
			"result":{"name":None,"price":None,"in_stock":True}},
			old={"name":"efg","price":9,"in_stock":False}),
			{"success":True,"result":{}})
		print("Test c_2_2: attendance_validator")

	def test_c_2_3_attendance_validator(self):	
		# new missing value
		self.assertEqual(attendance_validator(expected=
			{"name":"string","price":"integer","in_stock":"boolean"}
			,received={"success":True,
			"result":{"name":None,"price":5,"in_stock":True}}),
			{"success":False,"result":{"status":400,"description":
			"name is missing"}})
		
		# old missing all
		self.assertEqual(attendance_validator(expected=
			{"name":"string","price":"integer","in_stock":"boolean"}
			,received={"success":True,
			"result":{"name":None,"price":None,"in_stock":None}},
			old={"name":"efg","price":9,"in_stock":False}),
			{"success":False,"result":{"status":400,"description":
			"you must at least enter one field to change"}})
		print("Test c_2_3: attendance_validator")


	def test_c_2_4_attendance_validator(self):	
		# failing checkpoint
		try:
			attendance_validator(expected=
			{"name":"string","price":"integer","in_stock":"boolean"}
			,received={"success":1,
			"result":{"name":"abc","price":5,"in_stock":True}},
			old={"name":"efg","price":9,"in_stock":False})
		except Exception as e:
			self.assertEqual(str(e),"MoRBs:attendance_validator:ERROR: 'received['success']' is supposed to have the type of 'bool', but found type of '<class 'int'>' instead")
		# recieved not dict
		try:
			attendance_validator(expected=
			{"name":"string","price":"integer","in_stock":"boolean"}
			,received="abc",
			old={"name":"efg","price":9,"in_stock":False})
		except Exception as e:
			self.assertEqual(str(e),"MoRBs:attendance_validator:ERROR: 'received' is supposed to have the type of 'dict', but found type of '<class 'str'>' instead")
		print("Test c_2_4: attendance_validator")"""































# Make the tests conveniently executable
if __name__ == "__main__":
	unittest.main()