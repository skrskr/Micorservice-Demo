from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:root@db/main'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)


db = SQLAlchemy(app)
migrate = Migrate(app, db)



class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    title = db.Column(db.String(200))
    image = db.Column(db.String(200))
    

class ProductUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)

    UniqueConstraint('user_id', 'product_id', name="user_product_unique")


@app.route('/')
def index():
    return "hello"

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)