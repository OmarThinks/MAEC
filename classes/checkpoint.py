"""
Checkpoint

- Attributes:
 	- success:
 		- A boolean carring the value of True or False
 	- result:
 		- A dictionary carring info about what is next
 	- saModel:
 		- the SQLAlchemy model
 	- neglect: (default = None)
 		- fields of the column to be neglected
 		- None = neglect only the primary keys
 		- Example : ["id","price"]
 	- extra: list or None
 		- extra fields that are expected to be received
 		- Example ["page","sreach_name"]
	-EXAMPLE 1 :
		- Ckeckpoint.success = True
		- Ckeckpoint.result = {"price":10.01,"name":None}
		- Ckeckpoint.saModel = class: ....
		- Ckeckpoint.neglect = ["id","price"]
	-EXAMPLE 2 :
		- Ckeckpoint.success = False
		- Ckeckpoint.result = {"status":400,"description":
		"something went wrong", "validation_errors":[..]}
		- Ckeckpoint.saModel = class: ....
		- Ckeckpoint.neglect = ["id","price"]
- Inputs: 
	- success: Boolean
	- result: a dictionary
	- neglect: list or None (fields to be neglected)
	- result: a dictionary of the contained data
- Function:
	- if success = True:
		- Validate that each value of expected class has a 
			corresponding value of in result
	- if success = False:
		- validate that there is an integer status code
		- validate that description is a string
		- validation errors will not be validated
- Output:
	- there are no outputs
	- It is an object, it will be created
	- It will only raise error in case if there was an error
Tolerance:
	- No tolerance, these are developer's mistakes, not user input
"""

from errors import *
from classreader import check_received

class Ckeckpoint():
	"""docstring for Ckeckpoint"""
	def __init__(self, success, result,saModel,neglect=None,extra = None):
		# Making sure that success is Boolean
		expectDataType(function_name= "Checkpoint.__init__",
			variable_name = "success",expected_type=bool,
			input= success)
		# Making sure that result is dict
		expectDataType(function_name= "Checkpoint.__init__",
			variable_name = "result",expected_type=dict,
			input= result)
		if success == False:
			# Then we need result to have "status" and "description"
			expectDictKey(function_name="Checkpoint.__init__",
				variable_name = "result",expectedKey = "status",
				input = result)
			expectDictKey(function_name="Checkpoint.__init__",
				variable_name = "result",expectedKey = "description",
				input = result)
			# Now we need to validate that status is int 
			# and description is string or dict
			expectDataType(function_name= "Checkpoint.__init__",
			variable_name = "status",expected_type=int,
			input= result["status"])
			expectInRange(function_name="Checkpoint.__init__",
				variable_name="type(result['description'])",
				range=[str,dict],input=type(result['description']))

			self.success = success
			self.result = result
			self.saModel = saModel
			self.neglect = neglect
			self.extra = extra
			return

		# Now succes is boolean and True
		check_received(function_name="Ckeckpoint",
			saModel=saModel,received=result,neglect=neglect)
		if extra != None:
			expectInRange(function_name="Checkpoint.__init__",
				variable_name="type(extra)",
					range=[type(None),list],input=type(extra))
			for extra_field in extra:

				expectDataType(function_name="Checkpoint.__init__",
				variable_name="element in extra",
				expected_type=str,
				input=extra_field)

		self.success = success
		self.result = result
		self.saModel = saModel
		self.neglect = neglect
		self.extra = extra
