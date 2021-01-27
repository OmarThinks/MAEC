import unittest
from checkpoint import Ckeckpoint
from classreader import convert_class_to_dict
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy import (String, Integer, Float, Boolean)
from NotReceived import NotReceived

unittest.TestLoader.sortTestMethodsUsing = None

class checkpoint_TestCase(unittest.TestCase):

	def setUp(self):
		pass       
		
	
	def tearDown(self):
		"""Executed after reach test"""
		print("_+++++++++++++++++++++++++++++++++_")

	#Note: Tests are run alphapetically
	def test_0_test(self):
		self.assertEqual(1,1)
		print("Test 1:Hello, Tests!")



	def test_1_1_checkpoint(self):
		#Testing with a normal class
		Base = declarative_base()
		class saTestClass2(Base):
			__tablename__="hi"
			id = Column(Integer, primary_key=True, nullable=False)
			name = Column(String(63))
			price = Column(Float())
			in_stock = Column(Boolean())
		
		#success not boolean
		try:
			Ckeckpoint(success=1, result=1,saModel=1)
		except Exception as e:
			self.assertEqual(str(e),"MoRBs:Checkpoint."+
				"__init__:ERROR: 'success' is supposed "+
				"to have the type of 'bool', but found "+
				"type of '<class 'int'>' instead")
		#result not dict
		try:
			Ckeckpoint(success=False, result=1,saModel=1)
		except Exception as e:
			self.assertEqual(str(e),"MoRBs:Checkpoint."+
				"__init__:ERROR: 'result' is supposed "+
				"to have the type of 'dict', but found "+
				"type of '<class 'int'>' instead")
		# success= False, result has no Status
		try:
			Ckeckpoint(success=False, result={},saModel=1)
		except Exception as e:
			#print(str(e))
			self.assertEqual(str(e),"MoRBs:Checkpoint"+
				".__init__:ERROR:missing_data_error:"+
				"'result[status]' is missing")
		# success= False, result has no description
		try:
			Ckeckpoint(success=False, result={"status":"abc"},saModel=1)
		except Exception as e:
			#print(str(e))
			self.assertEqual(str(e),"MoRBs:Checkpoint"+
				".__init__:ERROR:missing_data_error:'"+
				"result[description]' is missing")
		# success= False, status not int
		try:
			Ckeckpoint(success=False, result=
				{"status":"abc","description":1},saModel=1)
		except Exception as e:
			#print(str(e))
			self.assertEqual(str(e),"MoRBs:Checkpoint."+
				"__init__:ERROR: 'status' is supposed "+
				"to have the type of 'int', but found "+
				"type of '<class 'str'>' instead")
		# success= False, description not string or dict
		try:
			Ckeckpoint(success=False, result=
				{"status":400,"description":1},saModel=1)
		except Exception as e:
			#print(str(e))
			self.assertEqual(str(e),"MoRBs:expectInRange"+
				":Checkpoint.__init__:ERROR:not_in_range_"+
				"error:'type(result['description'])' is "+
				"not in this range [<class 'str'>, "+
				"<class 'dict'>]")
		#success = False : successful
		cp = Ckeckpoint(success=False, result=
			{"status":400,"description":"abc"},saModel=1)
		self.assertEqual(convert_class_to_dict(cp),{'neglect': None, 
			'result': {'status': 400, 'description': 'abc'}, 
			'saModel': 1, 'success': False})
		#print(convert_class_to_dict(cp))
		print("Test 1_1:checkpoint")









# Make the tests conveniently executable
if __name__ == "__main__":
	unittest.main()