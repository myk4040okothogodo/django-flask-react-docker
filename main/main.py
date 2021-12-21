from flask import Flask, jsonify, abort
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
import requests
from producer import publish
from dataclasses import dataclass

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://mykmyk:mykmyk@db/main'
app.config["$DOCKERHOST"] = '172.21.0.1'
CORS(app)

db = SQLAlchemy(app)

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

    UniqueConstraint('user_id', 'product_id', name='user_product_unique')

@app.route('/api/products')
def index():
    return jsonify(Product.query.all())


@app.route('/api/products/<int:id>/like', methods=['POST'])
def like(id):
    req = requests.get('http://172.17.0.1:8000/api/user')
    print(req, type(req))
    json = req.json()

    try:
        productuser = ProductUser(user_id=json['id'], product_id=id)
        db.session.add(productuser)
        db.session.commit()
        #event
        publish('product_liked', id)
    except:
        abort(400, "You have already liked this product")


    return jsonify({
        'message':'success'  
        })
    

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
