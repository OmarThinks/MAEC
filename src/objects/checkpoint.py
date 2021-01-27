"""
Checkpoint

- Attributes:
 	- success:
 		A boolean carring the value of True or False
 	- result:
 		A dictionary carring info about what is next
	-EXAMPLE 1 :
		- Ckeckpoint.success = True
		- Ckeckpoint.result = {"price":10.01,"name":None}
	-EXAMPLE 2 :
		- Ckeckpoint.success = False
		- Ckeckpoint.result = {"status":400,"description":
		"something went wrong", "validation_errors":[..]}

- Inputs: 
	- success: Boolean
	- result: a dictionary
- Function:
	- if success = True:
		- Validate that each value of expected class has a 
			corresponding value of in result
	- if success = False:
		- validate that there is an integer status code
		- validate that description is a string
		- validation errors will not be validated
- Output:
	- It is an object, it will be created
	- It will only raise error in case if there was an error
Tolerance:
	- No tolerance, these are developer's mistakes, not user input
"""

class Ckeckpoint():
	"""docstring for Ckeckpoint"""
	def __init__(self, success, result):
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
			# and description is string
			expectDataType(function_name= "Checkpoint.__init__",
			variable_name = "status",expected_type=int,
			input= result["status"])
			expectDataType(function_name= "Checkpoint.__init__",
			variable_name = "description",expected_type=str,
			input= result["description"])
			self.success = success
			self.result = result
			return
		# Now succes is boolean and True
		expected = createExpectedFromClass(inputClass)
		validate_attendance_from_expected(
			input_dict= result,input_dict_name = "Checkpont.result",
			expected= expected)
		self.success = success
		self.result = result
	def ready():
		the_dict = self.result
		for key in the_dict:
			if the_dict[key] == None:
				raise Exception(
				"MoRBs:ERROR:Checkpoint:not ready, but found a value"+
				" of 'None' in this key:'" + str(key)+"'")

