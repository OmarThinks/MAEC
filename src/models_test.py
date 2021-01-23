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

import inspect
from sqlalchemy import Column as saColumn







"""


b:validation Functions


"""

unittest.TestLoader.sortTestMethodsUsing = None

class MoRBs_models_TestCase(unittest.TestCase):
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
	def test___a_test(self):
		self.assertEqual(1,1)
		print("Test 1:Hello, MoRBs Models Tests!")


	def test_a_01_001_validate_column_insert(self):
		col = Column("Hi","string", maximum=40, minimum = 7)
		self.assertEqual(col.name,"Hi")
		self.assertEqual(col.data_type,"string")
		self.assertEqual(col.maximum,40)
		self.assertEqual(col.minimum,7)
		self.assertEqual(col.primary_key,False)
		col = Column("Hi","string")
		self.assertEqual(col.primary_key,False)
		#name not string
		try:
			col = Column(1,"string")
		except Exception as e:
			self.assertEqual(str(e),"MoRBs:Column.__init__:ERROR: "+
				"'name' is supposed to have the type of 'string',"+
				" but found type of '<class 'int'>' instead")
		#data_type not string
		try:
			col = Column("price",123)
		except Exception as e:
			self.assertEqual(str(e),"MoRBs:Column.__init__:ERROR: "+
				"'data_type' is supposed to have the type of 'string',"+
				" but found type of '<class 'int'>' instead")
		#data_type not in supported
		try:
			col = Column("price","bla bla")
		except Exception as e:
			self.assertEqual(str(e),"MoRBs:Column.__init__:"+
				"ERROR:not_in_range_error:'data_type' is not in "+
				"this range "+str(DATA_TYPES_SUPPORTED))
		#name starts with '_'
		try:
			col = Column("_price","string")
		except Exception as e:
			self.assertEqual(str(e),"MoRBs:Column:_price:name"+
				":can not start with '_'")
		#name contains 'query'
		try:
			col = Column("thereisqueryhidden","string")
		except Exception as e:
			self.assertEqual(str(e),"MoRBs:Column:"+
				"thereisqueryhidden:name:can "+
				"not contain the string 'query'")
		#maximum not int
		try:
			col = Column("data","string", maximum = "abc")
		except Exception as e:
			self.assertEqual(str(e),"MoRBs:Column.__init__:ERROR:"+
				" 'maximum' is supposed to have the type of "+
				"'int', but found type of '<class 'str'>' instead")
		#minimum not int
		try:
			col = Column("data","string", minimum = "abc")
		except Exception as e:
			self.assertEqual(str(e),"MoRBs:Column.__init__:ERROR:"+
				" 'minimum' is supposed to have the type of "+
				"'int', but found type of '<class 'str'>' instead")
		#minimum > max
		try:
			col = Column("data","string", maximum = 10, minimum=40)
		except Exception as e:
			self.assertEqual(str(e),"MoRBs:Column:data"+
				":maximum can not be more than minimum")
		#private_key not bool
		try:
			col = Column("data","string", primary_key = "abc")
		except Exception as e:
			self.assertEqual(str(e),"MoRBs:Column.__init__:ERROR:"+
				" 'primary_key' is supposed to have the type of "+
				"'boolean', but found type of '<class 'str'>' instead")
		print("Test a_1_1: validate_column_insert")

	def test_a_01_002_validate_validate(self):
		col = Column("Hi","string")
		#in case of success string
		self.assertEqual(Column("Hi","string").validate("Hey"),
			{"success":True,"result":"Hey"})
		#in case of success float
		self.assertEqual(Column("Hi","float").validate("1.1"),
			{"success":True,"result":1.1})
		#in case of success integer
		self.assertEqual(Column("Hi","integer").validate("1"),
			{"success":True,"result":1})
		#in case of success boolean
		self.assertEqual(Column("Hi","boolean").validate(True),
			{"success":True,"result":True})
		
		#in case of failure integer
		self.assertEqual(Column("Hi","integer").validate("Hey"),
			{"success":False,"result":{"status":400,
			"description":"Hi can not be converted to integer"}})
		#in case of failure float
		self.assertEqual(Column("Hi","float").validate("Hey"),
			{"success":False,"result":{"status":400,
			"description":"Hi can not be converted to float"}})
		#in case of failure boolean
		self.assertEqual(Column("Hi","boolean").validate("Hey"),
			{"success":False,"result":{"status":400,
			"description":"Hi can not be converted to boolean"}})
		print("Test a_1_2: validate_column_validate")


	def test_a_1_3_oject_indces(self):	
		#print(Product)
		#print(Product.id)
		#print(Product.bla)
		class test_class():
			index1 ="abc"
			index2 ="efg"
			hiddenexpectedhere = 4567
			blablamorbshidden = 123
			def f1():
				pass
		self.assertEqual({"index1":"abc","index2":"efg"},
			convert_class_to_dict(test_class,case = "clean"))
		self.assertEqual({"index1":"abc","index2":"efg",
			"blablamorbshidden":123},
			convert_class_to_dict(test_class,case = "all"))
		self.assertEqual({"blablamorbshidden":123},
			convert_class_to_dict(test_class,case = "morbs"))
		print("Test a_1_3: oject_indces")

	def test_a_1_4_createExpectedFromClass(self):	
		class test_class():
			id = Column("id","integer",primary_key = True)
			name = Column("name","string")
			price = Column("price","float")
			hiddenexpectedhere = 4567
			hiddenexpectedher = Column("hiddenexpectedher","float")
			blablamorbshidden = Column("blablamorbshidden","float")
			def f1():
				pass
		self.assertEqual({"name":"string","price":"float"},
			createExpectedFromClass(test_class))
		print("Test a_1_4: createExpectedFromClass")
	
	def test_a_1_5_generateModelAttrs(self):	
		test_dict = {
			"id": Column("id","integer"),
			"name" : Column("name","string"),
			"price" : Column("price","float")
		}
		"""data = generateModelAttrs(test_dict)
		self.assertEqual(
			data["expected"],{"id":"integer",
			"name":"string","price":"float"})
		self.assertEqual(data["morbs"],test_dict)
		self.assertEqual(
			data["morbs"],{
			"id": Column("id","integer"),
			"name" : Column("name","string"),
			"price" : Column("price","float")})"""
		self.assertEqual(
			{"id":test_dict["id"].saColumn,
			"name":test_dict["name"].saColumn,
			"price":test_dict["price"].saColumn,
			"expected":{"id":"integer","name":"string","price":"float"},
			"morbs":{
			"id":test_dict["id"],
			"price":test_dict["price"],
			"name":test_dict["name"]
			}
			},
			generateModelAttrs(test_dict))
		print("Test a_1_5: generateModelAttrs")

	def test_a_1_6_Ckeckpoint(self):	
		class test_class():
			id = Column("id","integer",primary_key = True)
			name = Column("name","string")
			price = Column("price","float")
			hiddenexpectedhere = 4567
			hiddenexpectedher = Column("hiddenexpectedher","float")
			blablamorbshidden = Column("blablamorbshidden","float")
			def f1():
				pass
		cp = Ckeckpoint(success = True, result ={"name":"abc","price":None}, 
			inputClass = test_class)
		self.assertEqual(cp.success, True) 
		self.assertEqual(cp.result, {"name":"abc","price":None}) 
		cp = Ckeckpoint(success = False, result ={"status":400,
			"description":"error"}, 
			inputClass = test_class)
		self.assertEqual(cp.success, False) 
		self.assertEqual(cp.result, {"status":400, "description":"error"}) 
		try:
			Ckeckpoint(success = True)
		except Exception as e:
			pass
		print("Test a_1_6: Ckeckpoint")










# Make the tests conveniently executable
if __name__ == "__main__":
	unittest.main()
