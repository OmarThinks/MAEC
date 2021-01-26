"""
expected is an objects that looks consits of one variable
	- fields
		this is a list of the expected columns
		the only way to generate this is to provide the SQLAlchemy model
		 unput is not a SQLAlchemy model, it will raise an error 
"""


class expected:
	def __init__(self, saModel):
		pass
