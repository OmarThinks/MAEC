from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
SECRET = "abc"
DATA_TYPES_SUPPORTED=["string","integer","boolean"]
try:
	from .validaton import *
	from .error import *
	from .models import *
	from .generator import *
	from .test_app import *
except:
	from validation import *
	from error import *
	from models import *
	from generator import *
	from test_app import *
