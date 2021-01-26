from errors import expectInRange
import inspect
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.sql.schema import MetaData

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





def convert_sa_to_dict(saModel):

	convert_class_to_dict(input,case = "all")













"""
saColumnReader
- Inputs:
	- sqlalchmey_column:
		The SQLAlchemy column
- Function:
	- It will read the SQLAlchemy Column
- Outputs:
	- a dict of the attributes of this dictionary
- Example:

"""

def saColumnReader(sqlalchmey_column):
	expectDataType(function_name = "readSAColumn",
		variable_name = "sqlalchmey_column",
		expected_type = InstrumentedAttribute,
		input = sqlalchmey_column)
	toReturn = {}
	
	try:
		toReturn["autoincrement"]=sqlalchmey_column.comparator.autoincrement # auto
		toReturn["default"]=sqlalchmey_column.comparator.default # None
		toReturn["foreign_keys"]=sqlalchmey_column.comparator.foreign_keys # set()
		toReturn["key"]=sqlalchmey_column.comparator.key # id
		toReturn["name"]=sqlalchmey_column.comparator.name # id
		toReturn["nullable"]=sqlalchmey_column.comparator.nullable # False
		toReturn["primary_key"]=sqlalchmey_column.comparator.primary_key # True
		toReturn["type"]=sqlalchmey_column.comparator.type # INTEGER
		toReturn["unique"]=sqlalchmey_column.comparator.unique # None
	except:
		raise Exception("MoRBs:ERROR:readSAColumn:can not read this"+
			" column, may be this version of MoRBs is incompatible"+
			" with your version of SQLAlchemy")
	return toReturn


