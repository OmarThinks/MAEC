from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
SECRET = "abc"
DATA_TYPES_SUPPORTED=["string","integer","boolean"]

try:
	from .column import *
	from .validaton import *
	from .error import *
	from .models import *
	from .level1 import *
	from .test_app import *
except:
	from column import *
	from validation import *
	from error import *
	from models import *
	from level1 import *
	from test_app import *
