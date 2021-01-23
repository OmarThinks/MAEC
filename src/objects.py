try:
	from __init__ import *
except:
	from src import *
from sqlalchemy import Column as saColumn
import inspect


class Column():
	"""docstring for Column"""
	def __init__(self, name, data_type, maximum= 10000000000000000000, 
		minimum = -10000000000000000000, primary_key = False):
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
		if type(primary_key) != bool:
			data_type_error(function_name="Column.__init__",
				variable_name="primary_key",
				expected_type_name="boolean",input=primary_key)
		#setting up sa data type
		if data_type == "string":
			saCol = saColumn(db.String()#,nullable=False
				,primary_key=primary_key)
		elif data_type == "boolean":
			saCol = saColumn(db.Boolean()#,nullable=False
				,primary_key=primary_key)
		elif data_type == "float":
			saCol = saColumn(db.Float()#,nullable=False
				,primary_key=primary_key)
		elif data_type == "integer":
			saCol = saColumn(db.Integer()#,nullable=False
				,primary_key=primary_key)

		self.saColumn = saCol
		self.name = name
		self.data_type = data_type
		self.maximum = maximum		
		self.minimum = minimum		
		self.primary_key = primary_key
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





def modelGenerator(input):
	input_attrs = convert_class_to_dict(input,case = "clean")
	class toReturn(db.Model):
		pass			
	#for input_attrs in :
	#	pass
	#setattr(toReturn, 'deal_accepted', self.use_it)

	def __init__():
		class sample(db.Model):
			__tablename__ = 'sometable'
			id = Column("id","integer",primary_key = True).saColumn #saColumn(db.Integer, primary_key=True)
			name = Column("name","string",primary_key = False).saColumn #saColumn(db.String,primary_key=False)
		"""class example(db.Model):
			__tablename__ = 'sometable'
			id = Column("id","integer")"""
		#db.create_all()
		return sample
	return __init__()




class test_model():
	__tablename__ = "abc"
	id = Column(name = "id" , data_type = "integer")
	price = Column(name = "price" , data_type = "float")
	in_stock = Column(name = "in_stock" , data_type = "boolean")



#da = modelGenerator(test_model)













"""
convert_class_to_dict

- INPUTS: 
	- input : a class with attributes
		- Example:
			class example():
				name = "Labtop"
				price = 123
	- case : a string that carries one of three values
		- "all" : means return all attrs
		- "morbs": get all the attrs containging the word morbs
		- "clean": get all the attrs NOT containging the word morbs
- FUNCTION: create a dict that represents the class attributes
- OUTPUT: a dict that represents the class attrs and their values
	- Example: {"name":"Labtop","price":123}

"""
def convert_class_to_dict(input,case = "all"):
	expectInRange(function_name="convert_class_to_dict",variable_name="case"
		,range=["all","morbs", "clean"],input = case)
	data = inspect.getmembers(input, 
	lambda a:not(inspect.isroutine(a)))
	to_pop = []
	
	the_data = []
	for a in data:
		if not(a[0].startswith('_') 
		or a[0].endswith('_') or
		(a[0] == "query") or (a[0] == "query_class") or 
		("expected" in a[0])
		):
			the_data.append(a)
	toReturn = {}
	for element in the_data:		
		toReturn[element[0]] = element[1]
	#Now toReturn is full
	#To remove all key containng 'morbs'
	if case == "clean":
		for key in toReturn:
			if "morbs" in key:
				to_pop.append(key)
	
	#To remove all keys not containing 'morbs'
	if case == "morbs":
		for key in toReturn:
			if "morbs" not in key:
				to_pop.append(key)

	#poping useless info
	for key in to_pop:
		try:
			toReturn.pop(key)
		except Exception as e:
			pass
	#Finally
	return toReturn





"""
returnModelAttrs

- Inputs:
	- input_dict : a clean dict that contains the Columns
		- every element here must be of the Column type
		- { < column-name > : < Column > }
		- Example:
					{
					"id":Column(name="id",data_type="integer"),
					"name":Column(name="name",data_type="string")
					}
- Function:
	- Create a dictionary that represents the attrs of 
		the Final SQLAchemy model
	- a dict called 'morbs', that is the input
	- a dict called 'expected', to passed to reciever
	- raise error if something goes wrong
- Tolerance: None
	- These are developer mistakes, not user mistakes
- Output:
	a dictionary like this
	{
		< column-name > : < sq-Column >, ..., ...,
		"expected":{< column-name > : < data-type >, ..., ...},
		"morbs-Columns" : input_dict
	}
	-Example:
		{
			"id" : saCOlumn(db.Integer),
			"name" : saCOlumn(db.String),
			"expected": { "id" : "integer", "name" : "string" },
			"morbs-Columns" : {
					"id":Column(name="id",data_type="integer"),
					"name":Column(name="name",data_type="string")
					}
		}
"""
def generateModelAttrs(input_dict):
	for attribute in input_dict:
		if type(input_dict[attribute]) != Column:
			data_type_error(function_name="returnMORBSClass",
				variable_name=attribute,
				expected_type_name="Column",input = input_dict(attribute))



def createExpectedFromModel(inputModel):
	convert_class_to_dict(input,case = "all")

