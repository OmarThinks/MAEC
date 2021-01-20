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

try:
	from __init__ import *
except:
	from src import *





"""


b:validation Functions


"""

unittest.TestLoader.sortTestMethodsUsing = None

class MAECTestCase(unittest.TestCase):
	"""This class represents the trivia test case"""

	def setUp(self):
		# create and configure the app
		self.app = create_app(testing=True) #Flask(__name__)
		self.client = self.app.test_client
		#db.app = self.app
		#db.init_app(self.app)
		db.create_all()        
		
	
	def tearDown(self):
		"""Executed after reach test"""
		print("_+++++++++++++++++++++++++++++++++_")

	#Note: Tests are run alphapetically
	def test_a_test(self):
		self.assertEqual(1,1)
		print("Test 1:Hello, Tests!")



	def test_002_drop_all_create_all(self):
		db_drop_and_create_all()
		products = Product.query.all()
		self.assertEqual(len(products),0)
		print("Test 2: db_drop_and_create_all")


	def test_003_populate_tables(self):
		populate_tables()
		products = Product.query.all()
		self.assertEqual(len(products),6)
		print("Test 3: populate tables")





	def test_b_01_001_validate_model_id(self):
		all_products = Product.query
		validation = validate_model_id(input_id=1,
			model_query=all_products,
			model_name_string="product")
		self.assertEqual(validation["case"],1)
		self.assertEqual(all_products.get(1),
			validation["result"])
		print("Test b_1_1: validate_model_id: Product 1")

	def test_b_01_002_validate_model_id(self):
		all_products = Product.query
		validation = validate_model_id(input_id=6,
			model_query=all_products,
			model_name_string="product")
		self.assertEqual(validation["case"],1)
		self.assertEqual(all_products.get(6),
			validation["result"])
		print("Test b_1_2: validate_model_id: Product 6")

	def test_b_01_003_validate_model_id(self):
		all_products = Product.query
		validation = validate_model_id(input_id=5.5,
			model_query=all_products,
			model_name_string="product")
		self.assertEqual(validation["case"],1)
		self.assertEqual(all_products.get(5),
			validation["result"])
		print("Test b_1_3: validate_model_id: Product 5.5")

	def test_b_01_004_validate_model_id(self):
		all_products = Product.query
		validation = validate_model_id(input_id="3",
			model_query=all_products,
			model_name_string="product")
		self.assertEqual(validation["case"],1)
		self.assertEqual(all_products.get(3),
			validation["result"])
		print("Test b_1_4: validate_model_id: Product '3'")

	def test_b_01_005_validate_model_id(self):
		all_products = Product.query
		validation = validate_model_id(input_id="i",
			model_query=all_products,
			model_name_string="product")
		self.assertEqual(validation["case"],3)
		self.assertEqual("product id can not be"+
			" converted to integer"
			,validation["result"]["description"])
		self.assertEqual(400
			,validation["result"]["status"])
		print("Test b_1_5: validate_model_id: Product i")

	def test_b_01_006_validate_model_id(self):
		all_products = Product.query
		validation = validate_model_id(input_id=0,
			model_query=all_products,
			model_name_string="product")
		self.assertEqual(validation["case"],3)
		self.assertEqual("product id can not be less than"+
			" or equal to 0"
			,validation["result"]["description"])
		self.assertEqual(422
			,validation["result"]["status"])
		print("Test b_1_6: validate_model_id: Product 0")

	def test_b_01_007_validate_model_id(self):
		all_products = Product.query
		validation = validate_model_id(input_id=-1,
			model_query=all_products,model_name_string="product")
		self.assertEqual(validation["case"],3)
		self.assertEqual("product id can not be less than"+
			" or equal to 0"
			,validation["result"]["description"])
		self.assertEqual(422
			,validation["result"]["status"])
		print("Test b_1_7: validate_model_id: Product -1")

	def test_b_01_008_validate_model_id(self):
		all_products = Product.query
		validation = validate_model_id(input_id=20,
			model_query=all_products,
			model_name_string="product")
		self.assertEqual(validation["case"],2)
		self.assertEqual("there is no product with this id"
			,validation["result"]["description"])
		self.assertEqual(422
			,validation["result"]["status"])
		print("Test b_1_8: validate_model_id: Product 20")

	def test_b_01_009_validate_model_id(self):
		all_products = Product.query
		validation = validate_model_id(input_id=None,
			model_query=all_products,
			model_name_string="product")
		self.assertEqual(validation["case"],4)
		self.assertEqual({'status': 400, 'description': 'product is missing'},
			validation["result"])
		print("Test b_1_9: validate_model_id: Product None")













	def test_b_02_001_validate_string(self):
		to_validate = "to validate"
		validation = validate_string(
			input_string=to_validate,max_length=100,
			string_name="data")
		self.assertEqual(validation["case"],1)
		self.assertEqual("to validate",
			validation["result"])
		print("Test b_2_1: validate_string: 'to validate'")

	def test_b_02_002_validate_string(self):
		to_validate = 1
		validation = validate_string(
			input_string=to_validate,max_length=100,
			string_name="data")
		self.assertEqual(validation["case"],1)
		self.assertEqual("1",
			validation["result"])
		print("Test b_2_2: validate_string: '1'")

	def test_b_02_003_validate_string(self):
		to_validate = "More Than 3"
		validation = validate_string(
		input_string=to_validate,max_length=3,
			string_name="input")		
		self.assertEqual(validation["case"],2)
		self.assertEqual("maximum input length is 3 letters"
			,validation["result"]["description"])
		self.assertEqual(422
			,validation["result"]["status"])
		print("Test b_2_3: validate_string:"+
			" More than max length")

	def test_b_02_004_validate_string(self):
		to_validate = None
		validation = validate_string(
		input_string=to_validate,max_length=3,
			string_name="input")		
		self.assertEqual(validation["case"],3)
		self.assertEqual(validation["result"],None)
		print("Test b_2_4: validate_string:"+
			" None")









	def test_b_3_001_validate_boolean(self):
		validation = validate_boolean(input_boolean=True,
			input_name_string="variable")
		self.assertEqual(validation["case"],1)
		self.assertEqual(True,validation["result"])
		print("Test b_3_1: validate_boolean: True")

	def test_b_3_002_validate_boolean(self):
		validation = validate_boolean(input_boolean="True",
			input_name_string="variable")
		self.assertEqual(validation["case"],1)
		self.assertEqual(True,validation["result"])
		print("Test b_3_2: validate_boolean: 'True'")

	def test_b_3_003_validate_boolean(self):
		validation = validate_boolean(input_boolean="true",
			input_name_string="variable")
		self.assertEqual(validation["case"],1)
		self.assertEqual(True,validation["result"])
		print("Test b_3_3: validate_boolean: 'true'")

	def test_b_3_004_validate_boolean(self):
		validation = validate_boolean(input_boolean=1,
			input_name_string="variable")
		self.assertEqual(validation["case"],1)
		self.assertEqual(True,validation["result"])
		print("Test b_3_4: validate_boolean: 1")

	def test_b_3_005_validate_boolean(self):
		validation = validate_boolean(input_boolean="1",
			input_name_string="variable")
		self.assertEqual(validation["case"],1)
		self.assertEqual(True,validation["result"])
		print("Test b_3_5: validate_boolean: '1'")

	def test_b_3_006_validate_boolean(self):
		validation = validate_boolean(input_boolean=False,
			input_name_string="variable")
		self.assertEqual(validation["case"],1)
		self.assertEqual(False,validation["result"])
		print("Test b_3_6: validate_boolean: False")

	def test_b_3_007_validate_boolean(self):
		validation = validate_boolean(input_boolean="False",
			input_name_string="variable")
		self.assertEqual(validation["case"],1)
		self.assertEqual(False,validation["result"])
		print("Test b_3_7: validate_boolean: 'False'")

	def test_b_3_008_validate_boolean(self):
		validation = validate_boolean(input_boolean="false",
			input_name_string="variable")
		self.assertEqual(validation["case"],1)
		self.assertEqual(False,validation["result"])
		print("Test b_3_8: validate_boolean: 'false'")

	def test_b_3_009_validate_boolean(self):
		validation = validate_boolean(input_boolean=0,
			input_name_string="variable")
		self.assertEqual(validation["case"],1)
		self.assertEqual(False,validation["result"])
		print("Test b_3_9: validate_boolean: 0")

	def test_b_3_010_validate_boolean(self):
		validation = validate_boolean(input_boolean="0",
			input_name_string="variable")
		self.assertEqual(validation["case"],1)
		self.assertEqual(False,validation["result"])
		print("Test b_3_10: validate_boolean: '0'")

	def test_b_3_011_validate_boolean_wrong(self):
		validation = validate_boolean(input_boolean="5",
			input_name_string="variable")
		self.assertEqual(validation["case"],2)
		self.assertEqual("variable can not be "+
			"converted to boolean"
			,validation["result"]["description"])
		self.assertEqual(400
			,validation["result"]["status"])
		print("Test b_3_11: validate_boolean_wrong:"+
			" '5'")

	def test_b_3_012_validate_boolean(self):
		validation = validate_boolean(input_boolean=None,
			input_name_string="variable")
		self.assertEqual(validation["case"],3)
		self.assertEqual(None,validation["result"])
		print("Test b_3_12: validate_boolean: None")










	def test_b_4_001_validate_integer(self):
		validation = validate_integer(input_integer=5,
			input_name_string="input",maximum=1000,
			minimum=0)

		self.assertEqual(validation["case"],1)
		self.assertEqual(5.0,validation["result"])
		print("Test b_4_1: validate_integer: 5")

	def test_b_4_002_validate_integer(self):
		validation = validate_integer(input_integer=5.0,
			input_name_string="input",maximum=1000,
			minimum=0)

		self.assertEqual(validation["case"],1)
		self.assertEqual(5.0,validation["result"])
		print("Test b_4_2: validate_integer: 5.0")

	def test_b_4_003_validate_integer(self):
		validation = validate_integer(input_integer="5.0",
			input_name_string="input",maximum=1000,
			minimum=0)

		self.assertEqual(validation["case"],2)
		self.assertEqual("input can not be converted to integer"
			,validation["result"]["description"])
		self.assertEqual(400
			,validation["result"]["status"])
		print("Test b_4_3: validate_integer: '5.0'")

	def test_b_4_004_validate_integer_wrong(self):
		validation = validate_integer(input_integer="i",
			input_name_string="input",maximum=1000,
			minimum=0)

		self.assertEqual(validation["case"],2)
		self.assertEqual("input can not be converted to integer"
			,validation["result"]["description"])
		self.assertEqual(400
			,validation["result"]["status"])
		print("Test b_4_4: validate_integer: i")

	def test_b_4_005_validate_integer(self):
		validation = validate_integer(input_integer=0,
			input_name_string="input",maximum=1000,
			minimum=0)

		self.assertEqual(validation["case"],1)
		self.assertEqual(0.0,validation["result"])
		print("Test b_4_5: validate_integer: 0")

	def test_b_4_006_validate_integer_wrong(self):
		validation = validate_integer(input_integer=-40,
			input_name_string="input",maximum=1000,
			minimum=0)

		self.assertEqual(validation["case"],2)
		self.assertEqual("input can not be less than"+
			" 0"
			,validation["result"]["description"])
		self.assertEqual(422
			,validation["result"]["status"])
		print("Test b_4_6: validate_integer: -40")

	def test_b_4_007_validate_integer_wrong(self):
		validation = validate_integer(input_integer=4,
			input_name_string="input",maximum=3,
			minimum=0)

		self.assertEqual(validation["case"],2)
		self.assertEqual("input can not be more than"+
			" 3"
			,validation["result"]["description"])
		self.assertEqual(422
			,validation["result"]["status"])
		print("Test b_4_7: validate_integer: >max")

	def test_b_4_008_validate_integer_wrong(self):
		validation = validate_integer(input_integer=None,
			input_name_string="input",maximum=3,
			minimum=0)

		self.assertEqual(validation["case"],3)
		self.assertEqual(None
			,validation["result"])
		print("Test b_4_8: validate_integer: None")

























	def test_b_5_001_validate_float(self):
		validation = validate_float(input_float=5,
			input_name_string="input",maximum=1000,
			minimum=0)

		self.assertEqual(validation["case"],1)
		self.assertEqual(5.0,validation["result"])
		print("Test b_5_1: validate_float: 5")

	def test_b_5_002_validate_float(self):
		validation = validate_float(input_float=5.0,
			input_name_string="input",maximum=1000,
			minimum=0)

		self.assertEqual(validation["case"],1)
		self.assertEqual(5.0,validation["result"])
		print("Test b_5_2: validate_float: 5.0")

	def test_b_5_003_validate_float(self):
		validation = validate_float(input_float="5.0",
			input_name_string="input",maximum=1000,
			minimum=0)

		self.assertEqual(validation["case"],1)
		self.assertEqual(5.0,validation["result"])
		print("Test b_5_3: validate_float: '5.0'")

	def test_b_5_004_validate_float_wrong(self):
		validation = validate_float(input_float="i",
			input_name_string="input",maximum=1000,
			minimum=0)

		self.assertEqual(validation["case"],2)
		self.assertEqual("input can not be converted to float"
			,validation["result"]["description"])
		self.assertEqual(400
			,validation["result"]["status"])
		print("Test b_5_4: validate_float: i")

	def test_b_5_005_validate_float(self):
		validation = validate_float(input_float=0,
			input_name_string="input",maximum=1000,
			minimum=0)

		self.assertEqual(validation["case"],1)
		self.assertEqual(0.0,validation["result"])
		print("Test b_5_5: validate_float: 0")

	def test_b_5_006_validate_float_wrong(self):
		validation = validate_float(input_float=-40,
			input_name_string="input",maximum=1000,
			minimum=0)

		self.assertEqual(validation["case"],2)
		self.assertEqual("input can not be less than"+
			" 0"
			,validation["result"]["description"])
		self.assertEqual(422
			,validation["result"]["status"])
		print("Test b_5_6: validate_float: -40")

	def test_b_5_007_validate_float_wrong(self):
		validation = validate_float(input_float=4,
			input_name_string="input",maximum=3,
			minimum=0)

		self.assertEqual(validation["case"],2)
		self.assertEqual("input can not be more than"+
			" 3"
			,validation["result"]["description"])
		self.assertEqual(422
			,validation["result"]["status"])
		print("Test b_5_7: validate_float: >max")

	def test_b_5_008_validate_float_wrong(self):
		validation = validate_float(input_float=None,
			input_name_string="input",maximum=3,
			minimum=0)

		self.assertEqual(validation["case"],3)
		self.assertEqual(None
			,validation["result"])
		print("Test b_5_8: validate_float: None")


	def test_b_6_001_validate_base64(self):
		validation = validate_base64(input_string=None,
			input_name_string="input",maximum_length=4,
			minimum_length=0)
		self.assertEqual(validation,{"case":3,"result":None})
		
		validation = validate_base64(input_string=5,
			input_name_string="b64",maximum_length=4,
			minimum_length=0)
		self.assertEqual(validation,{"case":2,"result":
			{"description":"b64 is not a string","status":400}})

		validation = validate_base64(input_string="abcde",
			input_name_string="b64",maximum_length=4,
			minimum_length=0)
		self.assertEqual(validation,{"case":2,"result":
			{"description":"b64 length can not be more than 4 characters"
			,"status":422}})
		
		validation = validate_base64(input_string="a",
			input_name_string="b64",maximum_length=4,
			minimum_length=3)
		self.assertEqual(validation,{"case":2,"result":
			{"description":"b64 length can not be less than 3 characters"
			,"status":422}})
		
		validation = validate_base64(input_string="abcd",
			input_name_string="b64",maximum_length=4,
			minimum_length=3)
		self.assertEqual(validation,{"case":1,"result":"abcd"})
		
		validation = validate_base64(input_string="abcde",
			input_name_string="b64",maximum_length=8,
			minimum_length=3)
		self.assertEqual(validation,{"case":2,"result":
			{"description":"b64 can not be converted to base64"
			,"status":422}})
		
		validation = validate_base64(input_string="abc*",
			input_name_string="b64",maximum_length=8,
			minimum_length=3)
		self.assertEqual(validation,{"case":2,"result":
			{"description":"b64 can not be converted to base64"
			,"status":422}})
		
		validation = validate_base64(input_string="abcd",
			input_name_string="b64",maximum_length=8,
			minimum_length=3)
		self.assertEqual(validation,{"case":1,"result":"abcd"})
		print("Test b_6_1: validate_base64: None")


	def test_b_7_001_validate_specific(self):		
		validation = validate_specific(input_value="png",
			input_name_string="formatting",input_range=["png","jpg"])
		self.assertEqual(validation,{"case":1,"result":"png"})
		validation = validate_specific(input_value="a",
			input_name_string="formatting",input_range=["png","jpg"])
		self.assertEqual(validation,{"case":2,"result":
			{"description":"a is not allowed formatting",
			"status":422}})
		validation = validate_specific(input_value="abc",
			input_name_string="formatting",input_range=["png","jpg"])
		self.assertEqual(validation,{"case":2,"result":
			{"description":"abc is not allowed formatting",
			"status":422}})
		print("Test b_7_1: validate_specific:")







	def test_b_8_001_validate__must(self):
		validation = validate__must(input=5,type="f",
			input_name_string="my_data",maximum=1000,minimum=-5)
		self.assertEqual(validation["case"],True)
		self.assertEqual(5.0,validation["result"])
		print("Test b_8_1: validate__must float: 5")

	def test_b_8_002_validate__must(self):
		validation = validate__must(input="unknown",type="f",
			input_name_string="my_data",maximum=1000,minimum=-5)
		self.assertEqual(validation["case"],False)
		self.assertEqual("my_data can not be converted to float"
			,validation["result"]["description"])
		self.assertEqual(400
			,validation["result"]["status"])
		print("Test b_8_2: validate__must float: 'i'")

	def test_b_8_003_validate__must(self):
		validation = validate__must(input=5,type="i",
			input_name_string="my_data",maximum=1000,minimum=-5)
		self.assertEqual(validation["case"],True)
		self.assertEqual(5,validation["result"])
		print("Test b_8_3: validate__must integer: 5")

	def test_b_8_004_validate__must(self):
		validation = validate__must(input="unknown",type="i",
			input_name_string="my_data",maximum=1000,minimum=-5)
		self.assertEqual(validation["case"],False)
		self.assertEqual("my_data can not be converted to integer"
			,validation["result"]["description"])
		self.assertEqual(400
			,validation["result"]["status"])
		print("Test b_8_4: validate__must integer: 'i'")

	def test_b_8_005_validate__must(self):
		validation = validate__must(input=True,type="b",
			input_name_string="my_data",maximum=1000,minimum=-5)
		self.assertEqual(validation["case"],True)
		self.assertEqual(True,validation["result"])
		print("Test b_8_5: validate__must boolean: True")

	def test_b_8_006_validate__must(self):
		validation = validate__must(input="unknown",type="b",
			input_name_string="my_data",maximum=1000,minimum=-5)
		self.assertEqual(validation["case"],False)
		self.assertEqual("my_data can not be converted to boolean"
			,validation["result"]["description"])
		self.assertEqual(400
			,validation["result"]["status"])
		print("Test b_8_6: validate__must boolean: 'unknown'")

	def test_b_8_007_validate__must(self):
		validation = validate__must(input="dddaaatta",type="s",
			input_name_string="my_data",maximum=1000,minimum=-5)
		self.assertEqual(validation["case"],True)
		self.assertEqual("dddaaatta",validation["result"])
		print("Test b_8_7: validate__must string: 'dddaaatta'")

	def test_b_8_008_validate__must(self):
		try:
			validation = validate__must(input="1",type="wrong",
			input_name_string="my_data",maximum=1000,minimum=-5)
			self.assertEqual(True,False)
		except Exception as e:
			self.assertEqual(True,True)
		print("Test b_8_8: validate__must wrong type: 'wrong'")

	def test_b_8_009_validate__must(self):
		validation = validate__must(input=None,type="i",
			input_name_string="my_data",maximum=1000,minimum=-5)
		self.assertEqual(validation["case"],False)
		self.assertEqual("my_data is missing"
			,validation["result"]["description"])
		self.assertEqual(400
			,validation["result"]["status"])
		
		print("Test b_8_9: validate__must wrong input: None int")

	def test_b_8_010_validate__must(self):
		validation = validate__must(input=None,type="f",
			input_name_string="my_data",maximum=1000,minimum=-5)
		self.assertEqual(validation["case"],False)
		self.assertEqual("my_data is missing"
			,validation["result"]["description"])
		self.assertEqual(400
			,validation["result"]["status"])
		
		print("Test b_8_10: validate__must wrong input: None float")

	def test_b_8_011_validate__must(self):
		validation = validate__must(input=None,type="b",
			input_name_string="my_data",maximum=1000,minimum=-5)
		self.assertEqual(validation["case"],False)
		self.assertEqual("my_data is missing"
			,validation["result"]["description"])
		self.assertEqual(400
			,validation["result"]["status"])
		
		print("Test b_8_11: validate__must wrong input: None bool")

	def test_b_8_012_validate__must(self):
		validation = validate__must(input=None,type="s",
			input_name_string="my_data",maximum=1000,minimum=-5)
		self.assertEqual(validation["case"],False)
		self.assertEqual("my_data is missing"
			,validation["result"]["description"])
		self.assertEqual(400
			,validation["result"]["status"])	
		print("Test b_8_12: validate__must wrong input: None str")

	def test_b_8_013_validate__must(self):
		validation = validate__must(input="abcde",type="b64",
			input_name_string="b64",maximum=1000,minimum=-5)
		self.assertEqual(validation  ,{"case":False,"result":{"description":
		"b64 can not be converted to base64","status":422}})
		print("Test b_8_13: validate__must wrong input: wrong base64")

	def test_b_8_014_validate__must(self):
		validation = validate__must(input="abcd/+/=",type="b64",
			input_name_string="b64",maximum=1000,minimum=-5)
		self.assertEqual(validation  ,{"case":True,"result":"abcd/+/="})
		print("Test b_8_14: validate__must input: correct base64")

	def test_b_8_015_validate__must(self):
		validation = validate__must(input="png",input_name_string="formatting"
			,type="spfc",
			input_range=["png","jpg"])
		self.assertEqual(validation  ,{"case":True,"result":"png"})
		validation = validate__must(input="abc",input_name_string="formatting",
			type="spfc",
			input_range=["png","jpg"])
		self.assertEqual(validation  ,{"case":False,"result":
			{"description":"abc is not allowed formatting","status":422}})
		print("Test b_8_14: validate__must input: correct base64")



	def test_c_0_0_0(self):
		print("Here we start deep tests")

	def test_c_1_0_1_reciever_tests(self):
		#Testing the function of route "reciever/int"
		response = self.client().post("/reciever/1",json=None)
		#Expected to fail, there is no request body
		data = json.loads(response.data)
		#print(data)
		self.assertEqual(response.status_code,400)
		self.assertEqual(data["success"],True)
		self.assertIsNotNone(data["result"],"there is no request body")
		
	def test_c_1_0_2_reciever_tests(self):
		#Testing the function of route "reciever/int"
		response = self.client().post("/reciever/1",json=12)
		#Expected to fail, there is no request body
		data = json.loads(response.data)
		print(data)
		self.assertEqual(response.status_code,400)
		self.assertEqual(data["success"],True)
		self.assertIsNotNone(data["result"],"there is no request body")
		
























# Make the tests conveniently executable
if __name__ == "__main__":
	unittest.main()