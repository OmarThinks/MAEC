import unittest
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy import (String, Integer, Float, Boolean)
from errors import *

unittest.TestLoader.sortTestMethodsUsing = None

class errors_TestCase(unittest.TestCase):

	def setUp(self):
		pass       
		
	
	def tearDown(self):
		"""Executed after reach test"""
		print("_+++++++++++++++++++++++++++++++++_")

	#Note: Tests are run alphapetically
	def test_0000_test(self):
		self.assertEqual(1,1)
		print("Test 1:Hello, Tests!")



	def test_001_data_type_error(self):
		try:
			data_type_error("a","b","c","d")
		except Exception as e:
			self.assertEqual(str(e),
			"MoRBs:a:ERROR: 'b' is supposed to have the type"+
			" of 'c', but found type of '<class 'str'>' instead")
		print("Test 001: data_type_error")

	def test_002_missing_data_error(self):
		try:
			missing_data_error(function_name="sts",variable_name="tst")
		except Exception as e:
			self.assertEqual(str(e),
			"MoRBs:sts:ERROR:missing_data_error:'tst' is missing")
		print("Test 002: missing_data_error")

	def test_003_not_in_range_error(self):
		try:
			not_in_range_error(function_name="rty",
				variable_name="abc",range=["1","2"])
		except Exception as e:
			self.assertEqual(str(e),
			"MoRBs:rty:ERROR:not_in_range_error:'abc' "+
			"is not in this range ['1', '2']")
		print("Test 003: not_in_range_error")

	def test_004_expectDataType(self):
		expectDataType(function_name="tst",
			variable_name="abc",expected_type=int,input=789)
		try:
			expectDataType(function_name="tst",
				variable_name="abc",expected_type=dict,input=789)
		except Exception as e:
			self.assertEqual(str(e),
			"MoRBs:tst:ERROR: 'abc' is supposed to have the "+
			"type of 'dict', but found type of '<class 'int'>' instead")
		print("Test 004: expectDataType")

	def test_005_expectDictKey(self):
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
		print("Test 005: expectDictKey")

	def test_006_expectInRange(self):
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
			#print(str(e))
			self.assertEqual(str(e),
			"MoRBs:expectInRange:abc:ERROR:"+
			"not_in_range_error:'tst' is not in this range [1, 2, 3]")
		print("Test 006: expectInRange")


	def test_007_expect_sa_model(self):
		Base = declarative_base()
		class saTestClass1(Base):
			__tablename__="hi"
			id = Column(Integer, primary_key=True, nullable=False)
			name = Column(String(63))
		expect_sa_model(function_name="abc",saModel=saTestClass1)

		print("Test 007: expect_sa_model")






# Make the tests conveniently executable
if __name__ == "__main__":
	unittest.main()