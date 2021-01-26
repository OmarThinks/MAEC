






def saColumnReader(sacol):
	expectDataType(function_name = "readSAColumn",
		variable_name = "sacol",expected_type = InstrumentedAttribute,
		input = sacol)
	toReturn = {}
	
	try:
		toReturn["autoincrement"]=sacol.comparator.autoincrement # auto
		toReturn["default"]=sacol.comparator.default # None
		toReturn["foreign_keys"]=sacol.comparator.foreign_keys # set()
		toReturn["key"]=sacol.comparator.key # id
		toReturn["name"]=sacol.comparator.name # id
		toReturn["nullable"]=sacol.comparator.nullable # False
		toReturn["primary_key"]=sacol.comparator.primary_key # True
		toReturn["type"]=sacol.comparator.type # INTEGER
		toReturn["unique"]=sacol.comparator.unique # None
	except:
		raise Exception("MoRBs:ERROR:readSAColumn:can not read this"+
			" column, may be this version of MoRBs is incompatible"+
			" with your version of SQLAlchemy")
	return toReturn


