try:
    from __init__ import *
except:
    from src import *

import os
from sqlalchemy import Column, String, Integer, Float, Boolean
from flask_sqlalchemy import SQLAlchemy
import json





"""
def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
"""
'''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
    !!NOTE you can change the database_filename variable to 
        have multiple verisons of a database
'''





'''
Product
a persistent product entity, extends the base SQLAlchemy Model
id,name,price
'''
class Product(db.Model):
    # Autoincrementing, unique primary key
    id = Column(Integer(), primary_key=True)
    # String name
    name = Column(String(), unique=False, nullable=False)
    # name could be like "Labtop"
    # name dowsn't have to be unique
    # allowing several users to sell the same product
    price =  Column(Float(), unique=False, nullable=False)
    # Price is a float
    # Example: 5.0, 6.0 , 50.0, 0.5
    # It should be float, allowing things with low
    # price to be sold
    
    def __init__(self, price, name):
        self.name = name
        self.price = price
    '''
    insert()
        inserts a new model into a database
        the model must have a unique name
        the model must have a unique id or null id

    '''
    def insert(self):
        db.session.add(self)
        db.session.commit()
    '''
    delete()
        deletes a new model into a database
        the model must exist in the database
    '''
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    '''
    update()
        updates a new model into a database
        the model must exist in the database
    '''
    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(
        {
            'id': self.id,
            'name': self.name,
            'price': self.price
        })
    def simple(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price
        }

    def get_dict(self):
        return self.simple()































def db_drop_and_create_all():
    db.drop_all()
    db.create_all()



def populate_tables():
    db_drop_and_create_all()

    products = list()
    products.append(Product(
        name="Labtop", price=300))
    products.append(Product(
        name="Mobile", price=100))
    products.append(Product(
        name="Candy", price=.5))
    products.append(Product(
        name="Table", price=150))
    products.append(Product(
        name="Keyboard", price=5))
    products.append(Product(
        name="Mouse", price=4))
    db.session.add_all(products)
    db.session.commit()


