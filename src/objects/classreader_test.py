import unittest


from classreader import convert_class_to_dict

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
		class testClass(object):
			abc = 5
			def __init__():
				self.efg = 748
		
		self.assertEqual(convert_class_to_dict(testClass),{"abc":5})
		print("Test 1_1:convert_class_to_dict")














# Make the tests conveniently executable
if __name__ == "__main__":
	unittest.main()