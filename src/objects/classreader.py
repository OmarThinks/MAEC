from errors import expectInRange, expectDataType
import inspect
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.sql.schema import MetaData
from sqlalchemy.ext.declarative.api import DeclarativeMeta
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
def convert_class_to_dict(input):
	data = inspect.getmembers(input, 
	lambda a:not(inspect.isroutine(a)))
	to_pop = []
	
	the_data = []
	for a in data:
		if not(a[0].startswith('_') 
		or a[0].endswith('_') or
		(a[0] == "query") or (a[0] == "query_class")):
			the_data.append(a)
	toReturn = {}
	for element in the_data:		
		toReturn[element[0]] = element[1]
	return toReturn






"""
- Inputs:
	- saModel
		-This is SQLAlchemy model in the form of Base
- Function:
	- Read the columns of the SQLAlchemy model and 
- Output:
	- a dictionary containing all the columns
		-{"column name string": Column(..), ..}
Example:
	{
		"id":Column(Integer()),
		"name":Column(String()),
		...
	}
"""

def getSAModelColumns(saModel):
	expectDataType(function_name="getSAModelColumns",
		variable_name= saModel,expected_type = DeclarativeMeta,
		input=saModel)
	sa_dict = convert_class_to_dict(saModel)
	toReturn = {}
	for key in sa_dict:
		if type(sa_dict[key]) == InstrumentedAttribute:
			toReturn[key] = sa_dict[key]
	return toReturn













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
{'autoincrement': 'auto', 'constraints': set(), 'default': None, 
'foreign_keys': set(), 'key': 'id', 'name': 'id', 'nullable': False, 
'primary_key': True, 'type': Integer(), 'unique': None}
"""

def saColumnReader(sqlalchmey_column):
	expectDataType(function_name = "readSAColumn",
		variable_name = "sqlalchmey_column",
		expected_type = InstrumentedAttribute,
		input = sqlalchmey_column)
	toReturn = {}
	
	try:
		toReturn["autoincrement"]=sqlalchmey_column.comparator.autoincrement # auto
		toReturn["constraints"]=sqlalchmey_column.comparator.constraints # set()
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






"""
saModelColumnsNames
- Inputs:
	- saModel:
		The SQLAlchemy model
- Function:
	- It will return a list of the model columns names
- Outputs:
	- a list of the names of the columns
- Example:
	["id","name","price"]
"""

def saModelColumnsNames(saModel,expect_primary_keys=False):
	expectDataType(function_name="saModelColumnsNames",
		variable_name= "expect_primary_keys",expected_type=bool,
		input=expect_primary_keys)
	sa_cols = getSAModelColumns(saModel)
	cols_details = {}
	for key in sa_cols:
		cols_details[key] = saColumnReader(sa_cols[key])
	#sa_cols = [saColumnReader(a[key]) for a,key in enumerate(sa_cols)]
	toReturn = []
	for key in cols_details:
		if cols_details[key]["primary_key"] == True:
			if expect_primary_keys == False:
				continue
			toReturn.append(cols_details[key]["name"])
		else:
			toReturn.append(cols_details[key]["name"])
	return toReturn




"""
validate_attendance
- Inputs:
	- function_name(string): 
		the name of the function that called this function
	- saModel: the SQLAlchemy model, not an instance
	- received: a dictionary of the received values
		{<field_name>:<field_value>}
		- Example: {"name":"abc","price":None,"in_stock":NotReceived()}
	- expect_primary_keys:boolean default = False
		- a boolean that represents whether the primary_keys should be 
			expected or not
- Function:
	- Raise errors if something is missing (These are developer mistakes)
- Output: there is no return value, this is for validation only
Tolerance:
	- No tolerance, these are developer mistakes, not user inputs problem
"""
def validate_attendance(function_name,saModel,received,
	expect_primary_keys=False):
	expectDataType(
		function_name=str(function_name)+":validate_attendance",
		variable_name= "expect_primary_keys",expected_type=bool,
		input=expect_primary_keys)
	expected_names = saModelColumnsNames(saModel,expect_primary_keys)
	toReturn ={}
	for key in expected_names:
		expectDictKey(
			function_name=str(function_name)+":validate_attendance",
			variable_name= "received",expectedKey=key,
			input=received)
		toReturn[key] = received[key]
	return toReturn
			
