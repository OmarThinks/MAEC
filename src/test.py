try:
	from __init__ import *
except:
	from src import *

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








"""


b:validation Functions


"""

unittest.TestLoader.sortTestMethodsUsing = None

class MoRBs_TestCase(unittest.TestCase):
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









	def test_b_03_001_validate_boolean(self):
		validation = validate_boolean(input_boolean=True,
			input_name_string="variable")
		self.assertEqual(validation["case"],1)
		self.assertEqual(True,validation["result"])
		print("Test b_3_1: validate_boolean: True")

	def test_b_03_002_validate_boolean(self):
		validation = validate_boolean(input_boolean="True",
			input_name_string="variable")
		self.assertEqual(validation["case"],1)
		self.assertEqual(True,validation["result"])
		print("Test b_3_2: validate_boolean: 'True'")

	def test_b_03_003_validate_boolean(self):
		validation = validate_boolean(input_boolean="true",
			input_name_string="variable")
		self.assertEqual(validation["case"],1)
		self.assertEqual(True,validation["result"])
		print("Test b_3_3: validate_boolean: 'true'")

	def test_b_03_004_validate_boolean(self):
		validation = validate_boolean(input_boolean=1,
			input_name_string="variable")
		self.assertEqual(validation["case"],1)
		self.assertEqual(True,validation["result"])
		print("Test b_3_4: validate_boolean: 1")

	def test_b_03_005_validate_boolean(self):
		validation = validate_boolean(input_boolean="1",
			input_name_string="variable")
		self.assertEqual(validation["case"],1)
		self.assertEqual(True,validation["result"])
		print("Test b_3_5: validate_boolean: '1'")

	def test_b_03_006_validate_boolean(self):
		validation = validate_boolean(input_boolean=False,
			input_name_string="variable")
		self.assertEqual(validation["case"],1)
		self.assertEqual(False,validation["result"])
		print("Test b_3_6: validate_boolean: False")

	def test_b_03_007_validate_boolean(self):
		validation = validate_boolean(input_boolean="False",
			input_name_string="variable")
		self.assertEqual(validation["case"],1)
		self.assertEqual(False,validation["result"])
		print("Test b_3_7: validate_boolean: 'False'")

	def test_b_03_008_validate_boolean(self):
		validation = validate_boolean(input_boolean="false",
			input_name_string="variable")
		self.assertEqual(validation["case"],1)
		self.assertEqual(False,validation["result"])
		print("Test b_3_8: validate_boolean: 'false'")

	def test_b_03_009_validate_boolean(self):
		validation = validate_boolean(input_boolean=0,
			input_name_string="variable")
		self.assertEqual(validation["case"],1)
		self.assertEqual(False,validation["result"])
		print("Test b_3_9: validate_boolean: 0")

	def test_b_03_010_validate_boolean(self):
		validation = validate_boolean(input_boolean="0",
			input_name_string="variable")
		self.assertEqual(validation["case"],1)
		self.assertEqual(False,validation["result"])
		print("Test b_3_10: validate_boolean: '0'")

	def test_b_03_011_validate_boolean_wrong(self):
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

	def test_b_03_012_validate_boolean(self):
		validation = validate_boolean(input_boolean=None,
			input_name_string="variable")
		self.assertEqual(validation["case"],3)
		self.assertEqual(None,validation["result"])
		print("Test b_3_12: validate_boolean: None")










	def test_b_04_001_validate_integer(self):
		validation = validate_integer(input_integer=5,
			input_name_string="input",maximum=1000,
			minimum=0)

		self.assertEqual(validation["case"],1)
		self.assertEqual(5.0,validation["result"])
		print("Test b_4_1: validate_integer: 5")

	def test_b_04_002_validate_integer(self):
		validation = validate_integer(input_integer=5.0,
			input_name_string="input",maximum=1000,
			minimum=0)

		self.assertEqual(validation["case"],1)
		self.assertEqual(5.0,validation["result"])
		print("Test b_4_2: validate_integer: 5.0")

	def test_b_04_003_validate_integer(self):
		validation = validate_integer(input_integer="5.0",
			input_name_string="input",maximum=1000,
			minimum=0)

		self.assertEqual(validation["case"],2)
		self.assertEqual("input can not be converted to integer"
			,validation["result"]["description"])
		self.assertEqual(400
			,validation["result"]["status"])
		print("Test b_4_3: validate_integer: '5.0'")

	def test_b_04_004_validate_integer_wrong(self):
		validation = validate_integer(input_integer="i",
			input_name_string="input",maximum=1000,
			minimum=0)

		self.assertEqual(validation["case"],2)
		self.assertEqual("input can not be converted to integer"
			,validation["result"]["description"])
		self.assertEqual(400
			,validation["result"]["status"])
		print("Test b_4_4: validate_integer: i")

	def test_b_04_005_validate_integer(self):
		validation = validate_integer(input_integer=0,
			input_name_string="input",maximum=1000,
			minimum=0)

		self.assertEqual(validation["case"],1)
		self.assertEqual(0.0,validation["result"])
		print("Test b_4_5: validate_integer: 0")

	def test_b_04_006_validate_integer_wrong(self):
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

	def test_b_04_007_validate_integer_wrong(self):
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

	def test_b_04_008_validate_integer_wrong(self):
		validation = validate_integer(input_integer=None,
			input_name_string="input",maximum=3,
			minimum=0)

		self.assertEqual(validation["case"],3)
		self.assertEqual(None
			,validation["result"])
		print("Test b_4_8: validate_integer: None")

























	def test_b_05_001_validate_float(self):
		validation = validate_float(input_float=5,
			input_name_string="input",maximum=1000,
			minimum=0)

		self.assertEqual(validation["case"],1)
		self.assertEqual(5.0,validation["result"])
		print("Test b_5_1: validate_float: 5")

	def test_b_05_002_validate_float(self):
		validation = validate_float(input_float=5.0,
			input_name_string="input",maximum=1000,
			minimum=0)

		self.assertEqual(validation["case"],1)
		self.assertEqual(5.0,validation["result"])
		print("Test b_5_2: validate_float: 5.0")

	def test_b_05_003_validate_float(self):
		validation = validate_float(input_float="5.0",
			input_name_string="input",maximum=1000,
			minimum=0)

		self.assertEqual(validation["case"],1)
		self.assertEqual(5.0,validation["result"])
		print("Test b_5_3: validate_float: '5.0'")

	def test_b_05_004_validate_float_wrong(self):
		validation = validate_float(input_float="i",
			input_name_string="input",maximum=1000,
			minimum=0)

		self.assertEqual(validation["case"],2)
		self.assertEqual("input can not be converted to float"
			,validation["result"]["description"])
		self.assertEqual(400
			,validation["result"]["status"])
		print("Test b_5_4: validate_float: i")

	def test_b_05_005_validate_float(self):
		validation = validate_float(input_float=0,
			input_name_string="input",maximum=1000,
			minimum=0)

		self.assertEqual(validation["case"],1)
		self.assertEqual(0.0,validation["result"])
		print("Test b_5_5: validate_float: 0")

	def test_b_05_006_validate_float_wrong(self):
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

	def test_b_05_007_validate_float_wrong(self):
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

	def test_b_05_008_validate_float_wrong(self):
		validation = validate_float(input_float=None,
			input_name_string="input",maximum=3,
			minimum=0)

		self.assertEqual(validation["case"],3)
		self.assertEqual(None
			,validation["result"])
		print("Test b_5_8: validate_float: None")


	def test_b_06_001_validate_base64(self):
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


	def test_b_07_001_validate_specific(self):		
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







	def test_b_08_001_validate__must(self):
		validation = validate__must(input=5,type="f",
			input_name_string="my_data",maximum=1000,minimum=-5)
		self.assertEqual(validation["case"],True)
		self.assertEqual(5.0,validation["result"])
		print("Test b_8_1: validate__must float: 5")

	def test_b_08_002_validate__must(self):
		validation = validate__must(input="unknown",type="f",
			input_name_string="my_data",maximum=1000,minimum=-5)
		self.assertEqual(validation["case"],False)
		self.assertEqual("my_data can not be converted to float"
			,validation["result"]["description"])
		self.assertEqual(400
			,validation["result"]["status"])
		print("Test b_8_2: validate__must float: 'i'")

	def test_b_08_003_validate__must(self):
		validation = validate__must(input=5,type="i",
			input_name_string="my_data",maximum=1000,minimum=-5)
		self.assertEqual(validation["case"],True)
		self.assertEqual(5,validation["result"])
		print("Test b_8_3: validate__must integer: 5")

	def test_b_08_004_validate__must(self):
		validation = validate__must(input="unknown",type="i",
			input_name_string="my_data",maximum=1000,minimum=-5)
		self.assertEqual(validation["case"],False)
		self.assertEqual("my_data can not be converted to integer"
			,validation["result"]["description"])
		self.assertEqual(400
			,validation["result"]["status"])
		print("Test b_8_4: validate__must integer: 'i'")

	def test_b_08_005_validate__must(self):
		validation = validate__must(input=True,type="b",
			input_name_string="my_data",maximum=1000,minimum=-5)
		self.assertEqual(validation["case"],True)
		self.assertEqual(True,validation["result"])
		print("Test b_8_5: validate__must boolean: True")

	def test_b_08_006_validate__must(self):
		validation = validate__must(input="unknown",type="b",
			input_name_string="my_data",maximum=1000,minimum=-5)
		self.assertEqual(validation["case"],False)
		self.assertEqual("my_data can not be converted to boolean"
			,validation["result"]["description"])
		self.assertEqual(400
			,validation["result"]["status"])
		print("Test b_8_6: validate__must boolean: 'unknown'")

	def test_b_08_007_validate__must(self):
		validation = validate__must(input="dddaaatta",type="s",
			input_name_string="my_data",maximum=1000,minimum=-5)
		self.assertEqual(validation["case"],True)
		self.assertEqual("dddaaatta",validation["result"])
		print("Test b_8_7: validate__must string: 'dddaaatta'")

	def test_b_08_008_validate__must(self):
		try:
			validation = validate__must(input="1",type="wrong",
			input_name_string="my_data",maximum=1000,minimum=-5)
			self.assertEqual(True,False)
		except Exception as e:
			self.assertEqual(True,True)
		print("Test b_8_8: validate__must wrong type: 'wrong'")

	def test_b_08_009_validate__must(self):
		validation = validate__must(input=None,type="i",
			input_name_string="my_data",maximum=1000,minimum=-5)
		self.assertEqual(validation["case"],False)
		self.assertEqual("my_data is missing"
			,validation["result"]["description"])
		self.assertEqual(400
			,validation["result"]["status"])
		
		print("Test b_8_9: validate__must wrong input: None int")

	def test_b_08_010_validate__must(self):
		validation = validate__must(input=None,type="f",
			input_name_string="my_data",maximum=1000,minimum=-5)
		self.assertEqual(validation["case"],False)
		self.assertEqual("my_data is missing"
			,validation["result"]["description"])
		self.assertEqual(400
			,validation["result"]["status"])
		
		print("Test b_8_10: validate__must wrong input: None float")

	def test_b_08_011_validate__must(self):
		validation = validate__must(input=None,type="b",
			input_name_string="my_data",maximum=1000,minimum=-5)
		self.assertEqual(validation["case"],False)
		self.assertEqual("my_data is missing"
			,validation["result"]["description"])
		self.assertEqual(400
			,validation["result"]["status"])
		
		print("Test b_8_11: validate__must wrong input: None bool")

	def test_b_08_012_validate__must(self):
		validation = validate__must(input=None,type="s",
			input_name_string="my_data",maximum=1000,minimum=-5)
		self.assertEqual(validation["case"],False)
		self.assertEqual("my_data is missing"
			,validation["result"]["description"])
		self.assertEqual(400
			,validation["result"]["status"])	
		print("Test b_8_12: validate__must wrong input: None str")

	def test_b_08_013_validate__must(self):
		validation = validate__must(input="abcde",type="b64",
			input_name_string="b64",maximum=1000,minimum=-5)
		self.assertEqual(validation  ,{"case":False,"result":{"description":
		"b64 can not be converted to base64","status":422}})
		print("Test b_8_13: validate__must wrong input: wrong base64")

	def test_b_08_014_validate__must(self):
		validation = validate__must(input="abcd/+/=",type="b64",
			input_name_string="b64",maximum=1000,minimum=-5)
		self.assertEqual(validation  ,{"case":True,"result":"abcd/+/="})
		print("Test b_8_14: validate__must input: correct base64")

	def test_b_08_015_validate__must(self):
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

	def test_b_09_001_data_type_error(self):
		try:
			data_type_error("a","b","c","d")
		except Exception as e:
			self.assertEqual(str(e),
			"MoRBs:a:ERROR: 'b' is supposed to have the type"+
			" of 'c', but found type of '<class 'str'>' instead")
		print("Test b_9_001: data_type_error")

	def test_b_9_002_missing_data_error(self):
		try:
			missing_data_error(function_name="sts",variable_name="tst")
		except Exception as e:
			self.assertEqual(str(e),
			"MoRBs:sts:ERROR:missing_data_error:'tst' is missing")
		print("Test b_9_002: missing_data_error")

	def test_b_9_003_not_in_range_error(self):
		try:
			not_in_range_error(function_name="rty",
				variable_name="abc",range=["1","2"])
		except Exception as e:
			self.assertEqual(str(e),
			"MoRBs:rty:ERROR:not_in_range_error:'abc' "+
			"is not in this range ['1', '2']")
		print("Test b_9_003: not_in_range_error")

	def test_b_9_004_expectDataType(self):
		expectDataType(function_name="tst",
			variable_name="abc",expected_type=int,input=789)
		try:
			expectDataType(function_name="tst",
				variable_name="abc",expected_type=dict,input=789)
		except Exception as e:
			self.assertEqual(str(e),
			"MoRBs:tst:ERROR: 'abc' is supposed to have the "+
			"type of 'dict', but found type of '<class 'int'>' instead")
		print("Test b_9_004: expectDataType")

	def test_b_9_005_expectDictKey(self):
		expectDictKey(function_name="abc",variable_name="tst",
			expectedKey="123",input={"123":789,"456":"a"})
		#Not dict
		try:
			expectDictKey(function_name="abc",variable_name="tst",
				expectedKey="123",input=123)
		except Exception as e:
			self.assertEqual(str(e),
			"MoRBs:abc:ERROR: 'tst' is supposed to have the type "+
			"of 'dict', but found type of '<class 'int'>' instead")
		#key not string
		try:
			expectDictKey(function_name="abc",variable_name="tst",
				expectedKey=123,input={"123":789,"456":"a"})
		except Exception as e:
			self.assertEqual(str(e),
			"MoRBs:abc:ERROR: 'dictionary key:tst[123]' is"+
			" supposed to have the type of 'str', but found"+
			" type of '<class 'int'>' instead")
		#key not found
		try:
			expectDictKey(function_name="abc",variable_name="tst",
				expectedKey="1234",input={"123":789,"456":"a"})
		except Exception as e:
			self.assertEqual(str(e),
			"MoRBs:abc:ERROR:missing_data_error:'tst[1234]' is missing")
		print("Test b_9_005: expectDictKey")

	def test_b_9_010_expectInRange(self):
		expectInRange(function_name="abc",variable_name="tst",
			range=[1,2,3],input=1)
		#Not list
		try:
			expectInRange(function_name="abc",variable_name="tst",
				range={"abc":123},input=1)
		except Exception as e:
			self.assertEqual(str(e),
			"MoRBs:abc:ERROR: 'tst' is supposed to have the type "+
			"of 'list', but found type of '<class 'dict'>' instead")
		#Not in range
		try:
			expectInRange(function_name="abc",variable_name="tst",
				range=[1,2,3],input=4)
		except Exception as e:
			print(str(e))
			self.assertEqual(str(e),
			"MoRBs:expectInRange:abc:ERROR:"+
			"not_in_range_error:'tst' is not in this range [1, 2, 3]")
		print("Test b_9_010: expectInRange")

	"""def test_b_10_001_validate__dict(self):
		raise Exception("not ready")
		validate__dict({},"testing_function_name","test_name",full=True)
		validate__dict({"abc":"string","123":"integer","true":"boolean"}
			,"testing_function_name","test_name",full=True)
		validate__dict({"abc":"string","123":"integer","true":None}
			,"testing_function_name","test_name",full=False)
		try:
			validate__dict("abc","testing_function_name","test_name",full=True)
		except Exception as e:
			self.assertEqual(str(e),
			"MoRBs:validate__dict:ERROR: 'test_name' is supposed to have"+
			" the type of 'dict', but found type of '<class 'str'>' instead")
		try:
			validate_expected({"abc":123})
		except Exception as e:
			self.assertEqual(str(e),
			"MoRBs:validate_expected:ERROR: 'each element of expected'"+
			" is supposed to have the type of 'string', but found type "+
			"of '<class 'int'>' instead")
		try:
			validate_expected({"abc":"123"})
		except Exception as e:
			self.assertEqual(str(e),
			"MoRBs:validate_expected:ERROR: 123 is not a supported data type")
		print("Test b_10_1: validate_expected")"""


	def test_b_10_001_validate_expected(self):
		validate_expected({})
		validate_expected({"abc":"string","123":"integer","true":"boolean"})
		try:
			validate_expected("abc")
		except Exception as e:
			self.assertEqual(str(e),
			"MoRBs:validate_expected:ERROR: 'expected' is supposed to have "+
			"the type of 'dict', but found type of '<class 'str'>' instead")
		try:
			validate_expected({"abc":123})
		except Exception as e:
			self.assertEqual(str(e),
			"MoRBs:validate_expected:ERROR: 'each element of expected'"+
			" is supposed to have the type of 'string', but found type "+
			"of '<class 'int'>' instead")
		try:
			validate_expected({"abc":"123"})
		except Exception as e:
			self.assertEqual(str(e),
			"MoRBs:validate_expected:ERROR: 123 is not a supported data type")
		print("Test b_10_1: validate_expected")

	def test_b_11_001_validate_attendance_from_expected(self):
		#Exactly
		validate_attendance_from_expected(
			input_dict = {"a":1,"b":True},input_dict_name="tst",
			expected={"a":"string","b":"boolean"})
		#Empty
		validate_attendance_from_expected(
			input_dict = {},input_dict_name="tst",
			expected={})
		#More
		validate_attendance_from_expected(
			input_dict = {"a":1},input_dict_name="tst",
			expected={})
		try:
			#Expected got something wrong
			validate_attendance_from_expected(
				input_dict = {"a":1,"b":True},input_dict_name="tst",
			expected={"a":"bla_bla_blaaaaaaaa","b":"boolean"})
		except Exception as e:
			self.assertEqual(str(e),"MoRBs:validate_expected:ERROR: "+
				"bla_bla_blaaaaaaaa is not a supported data type")
		try:
			#input_dict got something wrong
			validate_attendance_from_expected(
				input_dict = {"a":1},input_dict_name="tst",
			expected={"a":"string","b":"boolean"})
		except Exception as e:
			self.assertEqual(str(e),"MoRBs:validate_attendance_from_expected:"+
				"ERROR:tst did not carry this key 'b', but it exists in"+
				" 'expected' dict")
		print("Test b_11_1: validate_attendance_from_expected")

	def test_b_12_001_new_attendance_validator(self):
		#Exactly
		self.assertEqual(new_attendance_validator(
			expected={"a":"string","b":"boolean"},
			received_result = {"a":1,"b":True}),
		{"success":True,"result":{"a":1,"b":True}})
		#Empty
		self.assertEqual(new_attendance_validator(
			expected={},received_result = {}),
		{"success":True,"result":{}})
		#More
		self.assertEqual(new_attendance_validator(
			expected={},received_result = {"a":1}),
		{"success":True,"result":{}})

		#fail validate attendance from expected
		try:
			self.assertEqual(new_attendance_validator(
			expected={"a":"string"},received_result = {}),
			{"success":False,"result":{"status":400, 
			"description":"a is missing"}})
		except Exception as e:
			self.assertEqual(str(e),
				"MoRBs:validate_attendance_from_expected:ERROR:"+
				"received did not carry this key 'a', but it exists in"+
				" 'expected' dict")
		print("Test b_12_1: new_attendance_validator")

	def test_b_13_001_validateReadyDict(self):
		#Exactly
		validateReadyDict(input_dict = {"a":1,"b":True},dict_name="tst")
		#Empty
		validateReadyDict(input_dict = {},dict_name="tst")
		#fail data type
		try:
			validateReadyDict(input_dict = "abc",dict_name="tst")
		except Exception as e:
			self.assertEqual(str(e),
				"MoRBs:validateReadyDict:ERROR: 'tst' is supposed to have"+
				" the type of 'dict', but found type of '<class 'str'>' instead")
		#fail value has None
		try:
			validateReadyDict(input_dict = {"a":1,"b":None},dict_name="tst")
		except Exception as e:
			self.assertEqual(str(e),
				"MoRBs:validateReadyDict:ERROR:tst:is "+
				"supposed to be a dictionary without 'None' values")
		print("Test b_13_1: validateReadyDict")

	def test_b_14_001_old_attendance_validator(self):
		#Exactly
		self.assertEqual(
		old_attendance_validator(expected={"a":"string","b":"integer"},
			received_result={"a":1,"b":5},old_dict={"a":4,"b":9}),
		{"success":True,"result":{"a":1,"b":5}})
		#Empty
		self.assertEqual(
		old_attendance_validator(expected={},received_result={},old_dict={}),
		{"success":True,"result":{}})
		self.assertEqual(
		old_attendance_validator(expected={},received_result={"a":4},
			old_dict={"b":"9"}),
		{"success":True,"result":{}})
		self.assertEqual(
		old_attendance_validator(expected={"a":"integer"},received_result={"a":None},
			old_dict={"a":"9"}),
		{"success":False,"result":{"status":400, 
				"description" : "you must at least enter one field to change"}})
		#missing value filled
		self.assertEqual(
		old_attendance_validator(expected={"a":"string","b":"integer"},
			received_result={"a":1,"b":None},old_dict={"a":4,"b":9}),
		{"success":True,"result":{"a":1,"b":9}})
		self.assertEqual(
		old_attendance_validator(expected={"a":"string","b":"integer"},
			received_result={"a":None,"b":7},old_dict={"a":"4","b":9}),
		{"success":True,"result":{"a":"4","b":7}})
		#fail: expected is wrong
		try:
			old_attendance_validator(expected={"abc":"str"},received_result={"a":4},
				old_dict={"b":"9"})
		except Exception as e:
			self.assertEqual(str(e),
				"MoRBs:validate_expected:ERROR: str is not a supported data type")
		#fail: received is wrong
		try:
			old_attendance_validator(expected={"abc":"string"},received_result={"a":4},
				old_dict={"abc":"9"})
		except Exception as e:
			self.assertEqual(str(e),
				"MoRBs:validate_attendance_from_expected:ERROR:received did "+
				"not carry this key 'abc', but it exists in 'expected' dict")
		#fail: old_dict is wrong
		try:
			old_attendance_validator(expected={"abc":"string"},
				received_result={"abc":4},
				old_dict={"abce":"9"})
		except Exception as e:
			self.assertEqual(str(e),
				"MoRBs:validate_attendance_from_expected:ERROR:old_dict did "+
				"not carry this key 'abc', but it exists in 'expected' dict")
		#fail: old_dict is not ready
		try:
			old_attendance_validator(expected={"abc":"string"},
				received_result={"abc":4},
				old_dict={"abc":None})
		except Exception as e:
			self.assertEqual(str(e),
				"MoRBs:validateReadyDict:ERROR:old_dict:is supposed "+
				"to be a dictionary without 'None' values")		
		#fail received is wrong
		try:
			validateReadyDict(input_dict = {"a":1,"b":None},dict_name="tst")
		except Exception as e:
			self.assertEqual(str(e),
				"MoRBs:validateReadyDict:ERROR:tst:is "+
				"supposed to be a dictionary without 'None' values")
		print("Test b_14_1: old_attendance_validator")

	def test_b_15_001_morbs_checkpoint(self):
		# Perfect
		morbs_checkpoint(input_dict={"success":True,"result":{}},
			function_name="tst",variable_name="nm")
		morbs_checkpoint(input_dict={"success":False,
			"result":{"status":1,"description":"abc"}},
			function_name="tst",variable_name="nm")
		#input_dict not dict
		try:
			morbs_checkpoint(input_dict=123,
			function_name="tst",variable_name="nm")
		except Exception as e:
			self.assertEqual(str(e),"MoRBs:tst:ERROR: 'nm' is supposed to have"+
				" the type of 'dict', but found type of '<class 'int'>' instead")
		#success not in input_dict
		try:
			morbs_checkpoint(input_dict={},function_name="tst",variable_name="nm")
		except Exception as e:
			self.assertEqual(str(e),"MoRBs:tst:ERROR:"+
				"missing_data_error:'nm['success']' is missing")
		#success not in input_dict
		try:
			morbs_checkpoint(input_dict={},function_name="tst",variable_name="nm")
		except Exception as e:
			self.assertEqual(str(e),"MoRBs:tst:ERROR:"+
				"missing_data_error:'nm['success']' is missing")
		#success not bool
		try:
			morbs_checkpoint(input_dict={"success":1},
				function_name="tst",variable_name="nm")
		except Exception as e:
			self.assertEqual(str(e),"MoRBs:tst:ERROR: 'nm['success']' "+
				"is supposed to have the type of 'bool', but found type "+
				"of '<class 'int'>' instead")
		#result not in
		try:
			morbs_checkpoint(input_dict={"success":True},
				function_name="tst",variable_name="nm")
		except Exception as e:
			self.assertEqual(str(e),"MoRBs:tst:ERROR:missing_data_"+
				"error:'nm['result']' is missing")
		#result not dict
		try:
			morbs_checkpoint(input_dict={"success":True,"result":123},
				function_name="tst",variable_name="nm")
		except Exception as e:
			self.assertEqual(str(e),"MoRBs:tst:ERROR: 'nm['result']' "+
				"is supposed to have the type of 'dict', but found type "+
				"of '<class 'int'>' instead")
		#missing status
		try:
			morbs_checkpoint(input_dict={"success":False,"result":{}},
				function_name="tst",variable_name="nm")
		except Exception as e:
			self.assertEqual(str(e),"MoRBs:tst:ERROR:missing_data_"+
				"error:'nm['result']['status']' is missing")
		#status not int
		try:
			morbs_checkpoint(input_dict={"success":False,"result":{"status":True}},
				function_name="tst",variable_name="nm")
		except Exception as e:
			self.assertEqual(str(e),"MoRBs:tst:ERROR: 'nm['result']"+
				"['status']' is supposed to have the type of 'int', "+
				"but found type of '<class 'bool'>' instead")
		#missing description
		try:
			morbs_checkpoint(input_dict={"success":False,"result":{"status":1}},
				function_name="tst",variable_name="nm")
		except Exception as e:
			self.assertEqual(str(e),"MoRBs:tst:ERROR:missing_data_error:"+
				"'nm['result']['description']' is missing")
		#description not string
		try:
			morbs_checkpoint(input_dict={"success":False,"result":
				{"status":1,"description":123}},
				function_name="tst",variable_name="nm")
		except Exception as e:
			self.assertEqual(str(e),"MoRBs:tst:ERROR: 'nm['result']['description']' is supposed to have the type of 'str', but found type of '<class 'int'>' instead")
		print("Test b_15_1: morbs_checkpoint")


	def test_c_0_0_0(self):
		print("Good MoRBs")

	def test_c_1_1_1_receiver_tests(self):
		#Testing the function of route "receiver_test/int"
		response = self.client().post("/receiver_test/1")
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
		print("Test c_2_4: attendance_validator")































# Make the tests conveniently executable
if __name__ == "__main__":
	unittest.main()