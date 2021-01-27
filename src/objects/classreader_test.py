import unittest
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.sql.schema import MetaData

from classreader import *
from sqlalchemy import Column
from sqlalchemy import (String, Integer, Float, Boolean)
from NotReceived import NotReceived

unittest.TestLoader.sortTestMethodsUsing = None

class classreader_TestCase(unittest.TestCase):

	def setUp(self):
		pass       
		
	
	def tearDown(self):
		"""Executed after reach test"""
		print("_+++++++++++++++++++++++++++++++++_")

	#Note: Tests are run alphapetically
	def test_0_test(self):
		self.assertEqual(1,1)
		print("Test 1:Hello, Tests!")



	def test_1_1_convert_class_to_dict(self):
		#Testing with a normal class
		class testClass():
			abc = 5
			def __init__(self):
				self.efg = 748
		#Testing the class itself
		self.assertEqual(convert_class_to_dict(testClass),{"abc":5})
		mytest = testClass()
		
		#Testing an instance of the class
		self.assertEqual(convert_class_to_dict(mytest),{"abc":5,"efg":748})
		print("Test 1_1:convert_class_to_dict")

	def test_1_1_convert_class_to_dict(self):
		#Testing with a normal class
		class testClass():
			abc = 5
			def __init__(self):
				self.efg = 748
		#Testing the class itself
		self.assertEqual(convert_class_to_dict(testClass),{"abc":5})
		mytest = testClass()
		
		#Testing an instance of the class
		self.assertEqual(convert_class_to_dict(mytest),{"abc":5,"efg":748})
		print("Test 1_1:convert_class_to_dict")

	


	def test_2_1_getSAModelColumns(self):
		#Testing with a SQLAlchemy declarative base class
		Base = declarative_base()
		class saTestClass2(Base):
			__tablename__="hi"
			id = Column(Integer, primary_key=True, nullable=False)
			name = Column(String(63))
		#Testing the class itself
		sa_dict = getSAModelColumns(saTestClass2)
		#print(len(sa_dict))
		self.assertEqual(len(sa_dict),2)
		for key in sa_dict:
			self.assertEqual(type(sa_dict[key]),InstrumentedAttribute)
		
		# Can not use code on instance
		"""mytest = saTestClass2(name= "abc")
		print(mytest)
		print(type(mytest))
		sa_dict = getSAModelColumns(mytest)
		print(sa_dict)
		self.assertEqual(len(sa_dict),2)
		for key in sa_dict:
			self.assertEqual(type(sa_dict[key]),
			InstrumentedAttribute)"""		
		print("Test 1_2:getSAModelColumns")

	def test_3_1_saColumnReader(self):
		#Testing with a SQLAlchemy declarative base class
		Base = declarative_base()
		class saTestClass3(Base):
			__tablename__="hi"
			id = Column(Integer, primary_key=True, nullable=False)
			name = Column(String(63))
		#Testing the class itself
		sa_dict = getSAModelColumns(saTestClass3)
		#print(saColumnReader(sa_dict["id"]))
		self.assertEqual(str(saColumnReader(sa_dict["id"])),
			"{'autoincrement': 'auto', 'constraints': set(),"+
			" 'default': None, 'foreign_keys': set(), "+
			"'key': 'id', 'name': 'id', 'nullable': False,"+
			" 'primary_key': True, 'type': Integer(),"+
			" 'unique': None}")
		print("Test 1_3:saColumnReader")

	def test_4_1_saModelColumnsNames(self):
		#Testing with a SQLAlchemy declarative base class
		Base = declarative_base()
		class saTestClass3(Base):
			__tablename__="hi"
			id = Column(Integer, primary_key=True, nullable=False)
			name = Column(String(63))
		columns_names = saModelColumnsNames(saTestClass3)
		self.assertEqual(saModelColumnsNames(saTestClass3),["name"])
		self.assertEqual(saModelColumnsNames(
			saTestClass3,expect_primary_keys=True),["id","name"])

		print("Test 1_4:saModelColumnsNames")

	def test_4_1_saModelColumnsNames(self):
		#Testing with a SQLAlchemy declarative base class
		Base = declarative_base()
		class saTestClass3(Base):
			__tablename__="hi"
			id = Column(Integer, primary_key=True, nullable=False)
			name = Column(String(63))
		columns_names = saModelColumnsNames(saTestClass3)
		self.assertEqual(saModelColumnsNames(saTestClass3),["name"])
		self.assertEqual(saModelColumnsNames(
			saTestClass3,expect_primary_keys=True),["id","name"])

		print("Test 1_4:saModelColumnsNames")

	def test_5_1_check_received(self):

		print("Test 1_5:check_received")


	def test_5_1_check_received(self):
		#Exactly
		Base = declarative_base()
		class saTestClass3(Base):
			__tablename__="hi"
			id = Column(Integer, primary_key=True, nullable=False)
			name = Column(String(63))
			price = Column(Float())
			in_stock = Column(Boolean())

		#Perfect
		check_received(function_name="tst",saModel=saTestClass3,
			received={"name":"abc","price":NotReceived,"in_stock":None},
			expect_primary_keys=False)
		#Perfect: expect_primary_keys = True
		check_received(function_name="tst",saModel=saTestClass3,
			received={"id":123,"name":"abc",
			"price":NotReceived,"in_stock":None},
			expect_primary_keys=True)
		#More
		check_received(function_name="tst",saModel=saTestClass3,
			received={"iddddddddddd":123,"name":"abc",
			"price":NotReceived,"in_stock":None},
			expect_primary_keys=False)

		"""check_received(
			input_dict = {"a":1,"b":True},input_dict_name="tst",
			expected={"a":"string","b":"boolean"})
		#Empty
		check_received(
			input_dict = {},input_dict_name="tst",
			expected={})
		#More
		check_received(
			input_dict = {"a":1},input_dict_name="tst",
			expected={})
		try:
			#Expected got something wrong
			check_received(
				input_dict = {"a":1,"b":True},input_dict_name="tst",
			expected={"a":"bla_bla_blaaaaaaaa","b":"boolean"})
		except Exception as e:
			self.assertEqual(str(e),"MoRBs:validate_expected:ERROR: "+
				"bla_bla_blaaaaaaaa is not a supported data type")
		try:
			#input_dict got something wrong
			check_received(
				input_dict = {"a":1},input_dict_name="tst",
			expected={"a":"string","b":"boolean"})
		except Exception as e:
			self.assertEqual(str(e),"MoRBs:check_received:"+
				"ERROR:tst did not carry this key 'b', but it exists in"+
				" 'expected' dict")"""
		print("Test 5_1: check_received")












# Make the tests conveniently executable
if __name__ == "__main__":
	unittest.main()