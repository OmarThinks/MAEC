try:
	from __init__ import *
except:
	from src import *


class Column():
	"""docstring for Column"""
	def __init__(self, name, data_type):
		if type(name) != str:
			data_type_error(function_name="Column.__init__",
				variable_name="name",expected_type_name="string",input=name)
		if type(data_type) != str:
			data_type_error(function_name="Column.__init__",
				variable_name="data_type",expected_type_name="string",input=name)
		if data_type not in DATA_TYPES_SUPPORTED:
			not_in_range_error(function_name="Column.__init__",
				variable_name="data_type",range=DATA_TYPES_SUPPORTED)
		if name[0] == "_":
			raise Exception("MoRBs:Column:name:can not start with '_'")
		if "query" in name:
			raise Exception("MoRBs:Column:name:can not contain"+
				" the string 'query'")
		self.name = name
		self.data_type = data_type
		


