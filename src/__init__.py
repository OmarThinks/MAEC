from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
SECRET = "abc"
DATA_TYPES_SUPPORTED=["string","integer","boolean","float"]

try:
	from .validaton import *
	from .error import *
	from .objects import *
	from .models import *
	from .level1 import *
	from .test_app import *
except:
	from validation import *
	from error import *
	from objects import *
	from models import *
	from level1 import *
	from test_app import *
