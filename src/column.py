import os
import secrets
import unittest
import json
import random
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func 
from flask_cors import CORS
from flask_migrate import Migrate 
import base64

import inspect

try:
	from __init__ import *
except:
	from src import *


class Column(object):
	"""docstring for Column"""
	def __init__(self, name, type):
		
		self.name = name
		self.type = type
		


