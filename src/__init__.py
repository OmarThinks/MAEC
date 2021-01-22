from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
SECRET = "abc"
try:
	from .validaton import *
	from .error import *
	from .models import *
	from .blocks import *
	from .test_app import *
except:
	from validation import *
	from error import *
	from models import *
	from blocks import *
	from test_app import *
