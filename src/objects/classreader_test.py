import unittest


unittest.TestLoader.sortTestMethodsUsing = None

class MoRBs_TestCase(unittest.TestCase):
	"""This class represents the trivia test case"""

	def setUp(self):
		pass       
		
	
	def tearDown(self):
		"""Executed after reach test"""
		print("_+++++++++++++++++++++++++++++++++_")

	#Note: Tests are run alphapetically
	def test_a_test(self):
		self.assertEqual(1,1)
		print("Test 1:Hello, Tests!")














# Make the tests conveniently executable
if __name__ == "__main__":
	unittest.main()