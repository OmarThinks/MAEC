from flask import Flask

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

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == "__main__":
    app.run()