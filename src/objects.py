try:
	from __init__ import *
except:
	from src import *
from sqlalchemy import Column as saColumn
from sqlalchemy import String, Integer, Float, Boolean


class Column():
	"""docstring for Column"""
	def __init__(self, name, data_type, maximum= 10000000000000000000, 
		minimum = -10000000000000000000):
		if type(name) != str:
			data_type_error(function_name="Column.__init__",
				variable_name="name",expected_type_name="string",input=name)
		if type(data_type) != str:
			data_type_error(function_name="Column.__init__",
				variable_name="data_type",
				expected_type_name="string",input=data_type)
		if data_type not in DATA_TYPES_SUPPORTED:
			not_in_range_error(function_name="Column.__init__",
				variable_name="data_type",range=DATA_TYPES_SUPPORTED)
		if name[0] == "_":
			raise Exception("MoRBs:Column:"+name+":name:can not start with '_'")
		if "query" in name:
			raise Exception("MoRBs:Column:"+name+":name:can not contain"+
				" the string 'query'")
		if type(maximum) != int:
			data_type_error(function_name="Column.__init__",
				variable_name="maximum",
				expected_type_name="int",input=maximum)
		if type(minimum) != int:
			data_type_error(function_name="Column.__init__",
				variable_name="minimum",
				expected_type_name="int",input=minimum)
		if minimum > maximum:
			raise Exception("MoRBs:Column:"+name+":maximum can"+
				" not be more than minimum")
		#setting up sa data type
		if data_type == "string":
			saCol = saColumn(db.String(),nullable=False)
		elif data_type == "boolean":
			saCol = saColumn(db.Boolean(),nullable=False)
		elif data_type == "float":
			saCol = saColumn(db.Float(),nullable=False)
		elif data_type == "integer":
			if name == "id":
				saCol = saColumn(db.Integer(),
					nullable=False,primary_key=True)
			else:
				self.saCol = saColumn(Integer(),nullable=False)

		self.saColumn = saColumn
		self.name = name
		self.data_type = data_type
		self.maximum = maximum		
		self.minimum = minimum		

	"""
	return value:

	"""
	def validate(self, input):
		validation_string = ""
		if self.data_type == "string":
			validation_string = "s"
		elif self.data_type == "integer":
			validation_string = "i"
		elif self.data_type == "boolean":
			validation_string = "b"
		elif self.data_type == "float":
			validation_string = "f"
		validation = validate__must(input = input,type = validation_string,
			input_name_string=self.name,maximum = self.maximum, 
			minimum=self.minimum)
		return {"success":validation["case"], 
		"result":validation["result"]}

