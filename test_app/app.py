from flask import Flask, jsonify
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, Float




app = Flask(__name__)
app.debug = True

Base = declarative_base()

class Product(Base):
	__tablename__ = 'products'
	id = Column(Integer, primary_key=True)
	name = Column(String)
	price = Column(Float)
	in_stock = Column(Boolean)
	
@app.route("/")
def home_route():
	return jsonify({"message":"Hi There!"}),200


if __name__ == "__main__":
	app.run()