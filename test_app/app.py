from flask import Flask, jsonify
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import Column, Integer, String, Boolean, Float




app = Flask(__name__)
app.debug = True

engine = create_engine('sqlite:///database/database.sqlite', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()


class Product(Base):
	__tablename__ = 'products'
	id = Column(Integer, primary_key=True)
	name = Column(String)
	price = Column(Float)
	in_stock = Column(Boolean)

Base.query = db_session.query_property()
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


	
@app.route("/")
def home_route():
	return jsonify({"type(Product)":str(type(Product)),
		"type(Product.id)":str(type(Product.id))}),200


if __name__ == "__main__":
	app.run()