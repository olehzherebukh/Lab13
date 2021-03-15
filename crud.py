from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'crud.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)


class GoodsOfPharmacy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price_of_good = db.Column(db.String(120), unique=True)
    nameOfGood = db.Column(db.String(120), unique=True)
    qualityOfGood = db.Column(db.String(120), unique=True)
    amountOfCustomersPerDay = db.Column(db.String(120), unique=True)
    typeOfGood = db.Column(db.String(120), unique=True)

    def __init__(self, priceOfGood, nameOfGood, qualityOfGood,
                 amountOfCustomersPerDay, typeOfGood):
        self.price_of_good = priceOfGood
        self.nameOfGood = nameOfGood
        self.qualityOfGood = qualityOfGood
        self.amountOfCustomersPerDay = amountOfCustomersPerDay
        self.typeOfGood = typeOfGood


class GoodSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('priceOfGood', 'nameOfGood', 'qualityOfGood', 'amountOfCustomersPerDay', 'typeOfGood')


good_schema = GoodSchema()
goods_schema = GoodSchema(many=True)


# endpoint to create new user
@app.route("/good", methods=["POST"])
def add_good():
    priceOfGood = request.json['priceOfGood']
    nameOfGood = request.json['nameOfGood']
    qualityOfGood = request.json['qualityOfGood']
    amountOfCustomersPerDay = request.json['amountOfCustomersPerDay']
    typeOfGood = request.json['typeOfGood']
    
    new_good = GoodsOfPharmacy(priceOfGood, nameOfGood, qualityOfGood, amountOfCustomersPerDay, typeOfGood)

    db.session.add(new_good)
    db.session.commit()

    return jsonify(new_good)


# endpoint to show all goods
@app.route("/good", methods=["GET"])
def get_good():
    all_goods = GoodsOfPharmacy.query.all()
    result = goods_schema.dump(all_goods)
    return jsonify(result.data)


# endpoint to get good detail by id
@app.route("/good/<id>", methods=["GET"])
def good_detail(id):
    good = GoodsOfPharmacy.query.get(id)
    return good_schema.jsonify(good)


# endpoint to update good
@app.route("/good/<id>", methods=["PUT"])
def good_update(id):
    good = GoodsOfPharmacy.query.get(id)
    priceOfGood = request.json['priceOfGood']
    nameOfGood = request.json['nameOfGood']
    qualityOfGood = request.json['qualityOfGood']
    amountOfCustomersPerDay = request.json['amountOfCustomersPerDay']
    typeOfGood = request.json['typeOfGood']

    good.price_of_good = priceOfGood
    good.nameOfGood = nameOfGood
    good.qualityOfGood = qualityOfGood
    good.amountOfCustomersPerDay = amountOfCustomersPerDay
    good.typeOfGood = typeOfGood

    db.session.commit()
    return good_schema.jsonify(good)


# endpoint to delete good
@app.route("/good/<id>", methods=["DELETE"])
def good_delete(id):
    good = GoodsOfPharmacy.query.get(id)
    db.session.delete(good)
    db.session.commit()

    return good_schema.jsonify(good)


if __name__ == '__main__':
    app.run(debug=True)
