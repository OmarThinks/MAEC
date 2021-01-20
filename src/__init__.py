from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

try:
	from .validaton import *
	from .error import *
	from .models import *
	from .test_app import *
except:
	from validation import *
	from error import *
	from models import *
	from test_app import *
