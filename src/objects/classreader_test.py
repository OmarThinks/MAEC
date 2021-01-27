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
	
		print("Test 1_2:getSAModelColumns")

	def test_3_1_get_sa_all_columns_names(self):
		#Testing with a SQLAlchemy declarative base class
		Base = declarative_base()
		class saTestClass2(Base):
			__tablename__="hi"
			id = Column(Integer, primary_key=True, nullable=False)
			name = Column(String(63))
		#Testing the class itself
		names = get_sa_all_columns_names(saTestClass2)
		self.assertEqual(names,["id","name"])
		print("Test 3_1:get_sa_all_columns_names")

	def test_4_1_validate_column_name_exists(self):
		#Testing with a SQLAlchemy declarative base class
		Base = declarative_base()
		class saTestClass2(Base):
			__tablename__="hi"
			id = Column(Integer, primary_key=True, nullable=False)
			name = Column(String(63))
		#These names really exist
		validate_column_name_exists(saTestClass2,"id")
		validate_column_name_exists(saTestClass2,"name")
		try:
			validate_column_name_exists(saTestClass2,"bla bla bla bla")			
		except Exception as e:
			self.assertEqual(str(e),"MoRBs:expectInRange:valid"+
				"ate_column_name_exists:ERROR:not_in_range_er"+
				"ror:'saColName' is not in this range ['id', 'name']")
		print("Test 4_1:validate_column_name_exists")

	def test_5_1_validate_columns_in_saModel(self):
		#Testing with a SQLAlchemy declarative base class
		Base = declarative_base()
		class saTestClass2(Base):
			__tablename__="hi"
			id = Column(Integer, primary_key=True, nullable=False)
			name = Column(String(63))
		#These names really exist
		validate_columns_in_saModel(saTestClass2,["id"])
		validate_columns_in_saModel(saTestClass2,["name","id"])
		
		#not string
		try:
			validate_columns_in_saModel(saTestClass2,[123])			
		except Exception as e:
			self.assertEqual(str(e),"MoRBs:validate_column_name"+
				"_exists:ERROR: 'saColName' is supposed to have "+
				"the type of 'str', but found type of "+
				"'<class 'int'>' instead")
		# does not exist
		try:
			validate_columns_in_saModel(saTestClass2,["123"])			
		except Exception as e:
			self.assertEqual(str(e),"MoRBs:expectInRange"+
				":validate_column_name_exists:ERROR:not_"+
				"in_range_error:'saColName' is not in this"+
				" range ['id', 'name']")
		print("Test 5_1:validate_columns_in_saModel")

	def test_6_1_saColumnReader(self):
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
		print("Test 6_1:saColumnReader")

	def test_7_1_sa_primary_keys_names(self):
		#Testing with a SQLAlchemy declarative base class
		Base = declarative_base()
		class saTestClass3(Base):
			__tablename__="hi"
			id = Column(Integer, primary_key=True, nullable=False)
			name = Column(String(63))
		self.assertEqual(sa_primary_keys_names(saTestClass3),["id"])
		print("Test 7_1:sa_primary_keys_names")

	def test_8_1_saModelColumnsNames(self):
		#Testing with a SQLAlchemy declarative base class
		Base = declarative_base()
		class saTestClass3(Base):
			__tablename__="hi"
			id = Column(Integer, primary_key=True, nullable=False)
			name = Column(String(63))
		# Default, neglect the primary keys only
		self.assertEqual(saModelColumnsNames(saTestClass3),["name"])
		#Neglect id
		self.assertEqual(saModelColumnsNames(
			saTestClass3,neglect=["id"]),["name"])
		#Neglect all
		self.assertEqual(saModelColumnsNames(
			saTestClass3,neglect=["id","name"]),[])
		#Not list
		try:
			saModelColumnsNames(saTestClass3,neglect=123)
		except Exception as e:
			self.assertEqual(str(e),"MoRBs:validate_columns"+
				"_in_saModel:ERROR: 'columns' is supposed to"+
				" have the type of 'list', but found type of"+
				" '<class 'int'>' instead")
		# a feild does not exist
		try:
			saModelColumnsNames(saTestClass3,neglect=["bla bla bla"])
		except Exception as e:
			self.assertEqual(str(e),"MoRBs:expectInRange:validate"+
				"_column_name_exists:ERROR:not_in_range_error:"+
				"'saColName' is not in this range ['id', 'name']")
		print("Test 8_1:saModelColumnsNames")

	def test_5_2_saModelColumnsNames(self):
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

		print("Test 5_2:saModelColumnsNames")

	def test_6_1_get_all_sa_columns_names(self):
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

		print("Test 5_2:saModelColumnsNames")







	def test_6_1_check_received(self):
		#Exactly
		Base = declarative_base()
		class saTestClass3(Base):
			__tablename__="hi"
			id = Column(Integer, primary_key=True, nullable=False)
			name = Column(String(63))
			price = Column(Float())
			in_stock = Column(Boolean())

		#Perfect
		check = check_received(function_name="tst",saModel=saTestClass3,
			received={"name":"abc","price":NotReceived,"in_stock":None},
			expect_primary_keys=False)
		self.assertEqual(check,{"name":"abc",
			"price":NotReceived,"in_stock":None})
		#Perfect: expect_primary_keys = True
		data = NotReceived()
		check = check_received(function_name="tst",saModel=saTestClass3,
			received={"id":123,"name":"abc",
			"price":data,"in_stock":None},
			expect_primary_keys=True)
		self.assertEqual(check,{"id":123,"name":"abc",
			"price":data,"in_stock":None})
		#More: iddddd was neglected because it is a primary key
		check = check_received(function_name="tst",saModel=saTestClass3,
			received={"iddddddddddd":123,"name":"abc",
			"price":data,"in_stock":None},
			expect_primary_keys=False)
		self.assertEqual(check,{"name":"abc",
			"price":data,"in_stock":None})

		try:
			#sa is not SQLAlchemy
			check_received(function_name="tst",saModel=123,
			received={"id":123,"name":"abc",
			"price":data,"in_stock":None},
			expect_primary_keys=True)
		except Exception as e:
			self.assertEqual(str(e),"MoRBs:getSAModel"+
				"Columns:ERROR: '123' is supposed to"+
				" have the type of 'DeclarativeMeta',"+
				" but found type of '<class 'int'>' instead")
		try:
			# received is not a dict
			check_received(function_name="tst",saModel=saTestClass3,
			received=123,
			expect_primary_keys=True)
		except Exception as e:
			self.assertEqual(str(e),"MoRBs:tst:"+
				"validate_received:ERROR: 'receiv"+
				"ed' is supposed to have the type "+
				"of 'dict', but found type of "+
				"'<class 'int'>' instead")
		print("Test 5_1: check_received")












# Make the tests conveniently executable
if __name__ == "__main__":
	unittest.main()