"""
expected is an objects that looks consits of one variable
	- fields
		this is a list of the expected columns
		the only way to generate this is to provide the SQLAlchemy model
		input is not a SQLAlchemy model, it will raise an error,
		ALL PRIMARY KEYS WILL NOT BE INCLUDED
	Example:
		- ["name", "price", "in_stock"]

"""


class Ckeckpoint():
	"""docstring for Ckeckpoint"""
	def __init__(self, success, result, inputClass):
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

