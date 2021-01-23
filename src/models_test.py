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
	def test_a_test(self):
		self.assertEqual(1,1)
		print("Test 1:Hello, MoRBs Models Tests!")


	def test_a_01_001_validate_column_insert(self):
		col = Column("Hi","string")
		self.assertEqual(col.name,"Hi")
		self.assertEqual(col.data_type,"string")
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
			self.assertEqual(str(e),"MoRBs:Column:thereisqueryhidden:name:can "+
				"not contain the string 'query'")
		#maximum not int
		try:
			col = Column("data","string", maximum = "abc")
		except Exception as e:
			self.assertEqual(str(e),"MoRBs:Column.__init__:ERROR: 'maximum' is supposed to have the type of 'int', but found type of '<class 'str'>' instead")

		print("Test a_1_1: validate_column_insert")

	def test_a_01_002_validate_validate(self):
		col = Column("Hi","string")
		self.assertEqual(col.validate("Hey"),
			{"success":True,"result":"Hey"})
		print("Test a_1_2: validate_column_validate")












# Make the tests conveniently executable
if __name__ == "__main__":
	unittest.main()
