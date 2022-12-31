from dataclasses import dataclass
import requests

from flask import Flask, jsonify, abort
from flask_migrate import Migrate
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint

from producer import publish


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:root@db/main'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)


db = SQLAlchemy(app)
migrate = Migrate(app, db)


@dataclass
class Product(db.Model):
    id: int
    title: str
    image: str
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    title = db.Column(db.String(200))
    image = db.Column(db.String(200))
    

@dataclass
class ProductUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)

    UniqueConstraint('user_id', 'product_id', name="user_product_unique")


@app.route('/api/products')
def index():
    return jsonify(Product.query.all())


@app.route('/api/products/<int:id>/like', methods=['POST'])
def like(id):
    req = requests.get("http://192.168.0.107:8000/api/user")
    data = req.json()
    try:
        product_user = ProductUser(user_id=data['id'], product_id=id)
        db.session.add(product_user)
        db.session.commit()
        # publish event
        publish("product_liked", id)
    except Exception as e:
        print(e)
        abort(400, "you already liked product")
    
    return jsonify({
        "message": "success"
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)