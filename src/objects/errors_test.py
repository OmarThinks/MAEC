import unittest

from errors import *

unittest.TestLoader.sortTestMethodsUsing = None

class errors_TestCase(unittest.TestCase):

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

		print("Test 1_1:convert_class_to_dict")







# Make the tests conveniently executable
if __name__ == "__main__":
	unittest.main()