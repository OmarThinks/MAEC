"""
def convert_class_to_dict(input)
def getSAModelColumns(saModel)
def get_sa_all_columns_names(saModel)
def validate_column_name_exists(saModel,saColName)
def validate_columns_in_saModel(saModel,columns)
def saColumnReader(sqlalchmey_column)
def sa_primary_keys_names(saModel)
def filteredSaModelColumnsNames(saModel,neglect=None)
def check_received(function_name,saModel,received,neglect=None)
def validate_fields(fields):
"""
"""
try:
	from __init__ import *
except:
	from .__init__ import *


#from .NotReceived import *
"""

try:
	from .NotReceived import NotReceived
	from .errors import *
except Exception as e:
	from NotReceived import NotReceived
	from errors import *

#from errors import *
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
	- Read the columns of the SQLAlchemy model and put it in a dict 
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
- Inputs:
	- saModel
		-This is SQLAlchemy model in the form of Base
- Function:
	- Read the columns of the SQLAlchemy model and put the names in a list
- Output:
	- a list containing all the names of the columns
		-{"column name string", "column name string", ...}
Example:
	["id","name","price"]
"""

def get_sa_all_columns_names(saModel):
	all_cols = getSAModelColumns(saModel)
	toReturn = []
	for key in all_cols:
		toReturn.append(key)
	return toReturn






"""
- Inputs:
	- saModel
		-This is SQLAlchemy model in the form of Base
	- saColName (string)
		- this is the string of the column name
		- Example: "id" 
- Function:
	- validate that there s a column with this name in the model
- Output:
	- No output
Tolerance:
	- No tolerance, these are developer mistakes, not user input
"""
def validate_column_name_exists(saModel,saColName):
	expectDataType(function_name="validate_column_name_exists",
		variable_name="saColName",expected_type=str,input=saColName)
	cols_names=get_sa_all_columns_names(saModel)
	expectInRange(function_name="validate_column_name_exists",
		variable_name="saColName",range=cols_names,input=saColName)




"""
- Inputs:
	- saModel
		-This is SQLAlchemy model in the form of Base
	- columns (list of strings)
		- this is the list of columns names
		- Example: ["id","name","price"] 
- Function:
	- validate that these names of columns really exist
- Output:
	- No output
Tolerance:
	- No tolerance, these are developer mistakes, not user input
"""
def validate_columns_in_saModel(saModel,columns):
	expectDataType(function_name = "validate_columns_in_saModel",
		variable_name = "columns",
		expected_type = list,
		input = columns)
	#Make sure that every element in columns is there in the model
	for name in columns:
		validate_column_name_exists(saModel,name)






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
	except Exception as e:
		raise Exception("MoRBs:ERROR:readSAColumn:can not read this"+
			" column, may be this version of MoRBs is incompatible"+
			" with your version of SQLAlchemy")
	return toReturn






"""
sa_primary_keys_names
- Inputs:
	- saModel:
		The SQLAlchemy model
- Function:
	- It will return a list of the names of the primary keys
- Outputs:
	- a list of primary keys
- Example:
	["id"]
"""
def sa_primary_keys_names(saModel):
	columns = getSAModelColumns(saModel)
	#Now columns look like this: {"id":Column(Integer),"name":...}
	toReturn = []
	for key in columns:
		if saColumnReader(columns[key])["primary_key"] == True:
			toReturn.append(key)
	return toReturn






"""
filteredSaModelColumnsNames
- Inputs:
	- saModel:
		- The SQLAlchemy model
	- neglect: list or None
		- the name of the fields to be neglected
		- Example: ["id","name"]
		- Default value is None, which means that it will neglect the
			primary keys
- Function:
	- It will return a list of the model columns names
- Outputs:
	- a list of the names of the columns
- Example:
	["id","name","price"]
"""
def filteredSaModelColumnsNames(saModel,neglect=None):
	#validate neglect
	if neglect == None:
		neglect = sa_primary_keys_names(saModel)
	else:
		validate_columns_in_saModel(saModel,neglect)
	
	#We need sa_cols to be like this ["id","name"]
	sa_cols = get_sa_all_columns_names(saModel)
	
	toReturn = []
	for col_name in sa_cols:
		if col_name not in neglect:
			toReturn.append(col_name)
	return toReturn


"""
check_received
- Inputs:
	- function_name(string): 
		the name of the function that called this function
	- saModel: the SQLAlchemy model, not an instance
	- received: a dictionary of the received values
		{<field_name>:<field_value>}
		- Example: {"name":"abc","price":None,"in_stock":NotReceived()}
	- neglect: list or None
		- the name of the fields to be neglected
		- Example: ["id","name"]
		- Default value is None, which means that it will neglect the
			primary keys
- Function:
	- Raise errors if something is missing (These are developer mistakes)
	- Raise error if a column is receved and it is not expected
- Output: there is no return value, this is for validation only
Tolerance:
	- No tolerance, these are developer mistakes, not user inputs problem
"""
def check_received(function_name,saModel,received,neglect=None):
	# received should be a dict
	expectDataType(
		function_name=str(function_name)+":check_received",
		variable_name= "received",expected_type=dict,
		input=received)

	sa_cols_names = filteredSaModelColumnsNames(saModel,neglect)
	#Now the sa_cols_names ook like this: ["id","name","price"]

	for column_name in sa_cols_names:
		expectDictKey(function_name=function_name,
			variable_name="received",expectedKey=column_name,
			input = received)
	#Now for every expected col in sa_model there must be a 
	# received value

	# Validating the opposite
	for key in received:
		expectInRange(function_name=function_name,
			variable_name = "received["+str(key)+"]",
			range=sa_cols_names,input=key)
