try:
	from __init__ import *
except:
	from src import *
from sqlalchemy import Column as saColumn
import inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (String, Integer, Float, Boolean)


def saColumnReader(sacol):
	expectDataType(function_name = "readSAColumn",
		variable_name = "sacol",expected_type = saColumn,
		input = sacol)
	toReturn = {}
	try:
		toReturn["autoincrement"]=saColumn.comparator.autoincrement
		toReturn["default"]=saColumn.comparator.default
		toReturn["autoincrement"]=saColumn.comparator.autoincrement
		toReturn["foreign_keys"]=saColumn.comparator.foreign_keys
		toReturn["key"]=saColumn.comparator.key
		toReturn["name"]=saColumn.comparator.name
		toReturn["nullable"]=saColumn.comparator.nullable
		toReturn["primary_key"]=saColumn.comparator.primary_key
		toReturn["type"]=saColumn.comparator.type
		toReturn["unique"]=saColumn.comparator.unique
	except:
		raise Exception("MoRBs:ERROR:readSAColumn:can not read this"+
			" column, may be this version of MoRBs is incompatible"+
			" with your version of SQLAlchemy")
	return toReturn




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










"""
def modelGenerator(database,inputClass):
	input_attrs = convert_class_to_dict(input,case = "clean")
"""
"""
	class MoRBsORM(db.Model):
		__tablename__ = "testit"
	# This is the dictionary of the attributes
	# {"id":saColumn(..),.....,
	#	"morbs": ... ,
	#	"expected": {name":"string"}}
	morbs_attrs = generateModelAttrs(input_dict)
	for attribute in morbs_attrs:
		setattr(MoRBsORM,attribute,morbs_attrs[attribute])
"""		
"""
	#for input_attrs in :
	#	pass
	#setattr(toReturn, 'deal_accepted', self.use_it)
	
	#def __init__():
"""
"""
	class sample(db.Model):
		__tablename__ = inputClass.__name__
		#__name__ = inputClass.__name__
		#__table_args__ = {'extend_existing': True}
		id = Column("id","integer", primary_key = True).saColumn #saColumn(db.Integer, primary_key=True)
		name = Column("name","string").saColumn #saColumn(db.String,primary_key=False)
"""
"""		
		class example(db.Model):
			__tablename__ = 'sometable'
			id = Column("id","integer")
		db.create_all()
		return sample
"""
"""
	#return sample
"""












"""
convert_class_to_dict

- INPUTS: 
	- input : a class with attributes
		- Example:
			class example():
				name = "Labtop"
				price = 123
				expected = "abc" # this will be removed
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
	- input_dict : the output of convert_class_to_dict
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
			"id" : saColumn(db.Integer),
			"name" : saColumn(db.String),
			"expected": { "id" : "integer", "name" : "string" },
			"morbs" : {
					"id":Column(name="id",data_type="integer"),
					"name":Column(name="name",data_type="string")
					}
		}
"""
def generateModelAttrs(input_dict):
	toReturn = {}
	toReturn["morbs"] = input_dict
	toReturn["expected"] = createExpectedFromColumnsDict(input_dict)
	for attribute in input_dict:
		toReturn[attribute] = input_dict[attribute].saColumn
	return toReturn


"""
createExpectedFromClass

- Inputs:
	- inputClass: trhe class that the user generated
		- Example:
			class tst():
				id = Column(data_type = "integer", 
					primary_key = True)
				name = Column(data_type = "string")
- Function:
	- Create the expected of the class
	- If the class got something wrong, it will evade it
- Output:
	- the expected dictionary
	-Example: {"id":"integer","name":"string"}
- Tolerance:
	- None
	- these are developer mistakes, not user inputs
"""


def createExpectedFromClass(inputClass):
	the_dict = convert_class_to_dict(inputClass,case = "clean")
	return createExpectedFromColumnsDict(the_dict)

def createExpectedFromColumnsDict(inputDict):
	the_dict = inputDict
	toReturn = {}
	for attributeName in the_dict:
		try:
			expectDataType(function_name="createExpectedFromClass",
			variable_name = attributeName,expected_type=Column,
			input=the_dict[attributeName])
		except:
			continue
		if the_dict[attributeName].primary_key == True:
			continue
		dataName = the_dict[attributeName].name
		dataType = the_dict[attributeName].data_type
		toReturn[dataName] = dataType
	return toReturn








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
		"something went wrong"}
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
- Output:
	- It is an object, it will be created
	- It will only raise error in case if there was an error
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





class MorbModel():
	"""docstring for MorbModel"""
	def setParents(database,model):
		setattr(model, '__mro__', (database.Model,MorbModel))






"""
Inputs:
	- db: this is the databse variable
	- model: this is the SQLAlchemy model
Function:
	- appending the attributes 'morbs' and 'expected' to it
	- appending these methods:
		- "__init__"
		- "morbs_init"
		- "morbsInsert"
		- "morbsDelete"
Output:
	- the same model after appending the attributes to it
Example:
	class Order(db.Model):
	    id = Column(Integer(), primary_key=True)
	    amount =  Column(Integer(), nullable=False)
	Order = morbsModel( Order )

"""

def getMorbsModel(db, model):
	"""input_attrs = convert_class_to_dict(input,case = "clean")
	class toReturn(db.Model):
		pass			
	"""
	#setattr(model,"tssssssssssssssst","123") 
	input_attrs_dict = convert_class_to_dict(model)
	input_attrs = generateModelAttrs(input_attrs_dict)
	for key in input_attrs:
		setattr(model,key,input_attrs[key])
	#setattr(model, '__mro__', (database.Model))
	table = convert_class_to_dict(model)

	#the_name=model.__name__
	#for input_attrs in :
	#	pass
	#setattr(toReturn, 'deal_accepted', self.use_it)
	"""class blueprint():
		pass
	input_attrs_dict = convert_class_to_dict(model,case = "clean")
	input_attrs = generateModelAttrs(input_attrs_dict)
	for key in input_attrs:
		setattr(blueprint,key,input_attrs[key])"""
	#setattr(blueprint,"id",Column("id","integer",primary_key = True).saColumn)
	#print(convert_class_to_dict(blueprint))
	#def __init__():
	"""class sample(Base,blueprint):
		#__table__ = the_name
		__tablename__ = the_name
		__name__ = the_name"""
		#id = Column("id","integer",primary_key = True).saColumn #saColumn(db.Integer, primary_key=True)
		#name = Column("name","string",primary_key = False).saColumn #saColumn(db.String,primary_key=False)
		#morbs = {"abc":"abc"}
		#expected = {"abc","abc"}
	#print(sample.a)
	#setattr(sample,"id",Column("id","integer",primary_key = True).saColumn)
	#input_attrs = convert_class_to_dict(input,case = "clean")
	"""for attr in input_attrs:
		setattr(sample, attr, input_attrs[attr])"""		
	"""class example(db.Model):
		__tablename__ = 'sometable'
		id = Column("id","integer")"""
	#db.create_all()
	#convert_class_to_dict(sample)
	#print(convert_class_to_dict(sample))
	#print(sample.morbs)
	#print(sample.expected)
	#return sample
	#return __init__()
	
	return model



class sample(db.Model):
	__tablename__ = 'sometable'
	id = Column("id","integer",primary_key = True).saColumn #saColumn(db.Integer, primary_key=True)
	name = Column("name","string",primary_key = False).saColumn #saColumn(db.String,primary_key=False)

def change_sample(model):
	morbs_dict = {
	"id":Column("id","integer",primary_key = True),
	"name":Column("name","string",primary_key = False)
	}
	return model





#sample = change_sample(sample)
#print(inspect(sample))



class test_model():
	__tablename__ = "abc"
	id = Column(name = "id" , data_type = "integer", primary_key =True)
	price = Column(name = "price" , data_type = "float")
	in_stock = Column(name = "in_stock" , data_type = "boolean")




class test_model2():
	id = Column(name = "id" , data_type = "integer", primary_key =True)
	priceee = Column(name = "priceeeee" , data_type = "float")
	in_stockeee = Column(name = "in_stockeeee" , data_type = "boolean")








#print(convert_class_to_dict(test_model))

#print("+++++++++")
#test_model = modelGenerator(database = db,model= test_model)
#test_model.setParents(db,test_model)
#da2 = modelGenerator(database = db,model= test_model2)
"""

"""

"""
"""