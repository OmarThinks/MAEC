import unittest
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.sql.schema import MetaData

from classreader import convert_class_to_dict, getSAModelColumns
from sqlalchemy import Column
from sqlalchemy import (String, Integer, Float, Boolean)

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
		class saTestClass(Base):
			__tablename__="hi"
			id = Column(Integer, primary_key=True, nullable=False)
			name = Column(String(63))
		#Testing the class itself
		sa_dict = getSAModelColumns(saTestClass)
		self.assertEqual(len(sa_dict),2)
		for key in sa_dict:
			self.assertEqual(type(sa_dict[key]),InstrumentedAttribute)
		
		mytest = saTestClass(name= "abc")
		sa_dict = getSAModelColumns(mytest)
		for key in sa_dict:
			self.assertEqual(type(sa_dict[key]),InstrumentedAttribute)		
		print("Test 1_2:getSAModelColumns")














# Make the tests conveniently executable
if __name__ == "__main__":
	unittest.main()