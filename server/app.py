#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries_list = []
    bakeries = Bakery.query.all()
    bakeries_list = [bakery.to_dict() for bakery in bakeries]
    return make_response(bakeries_list)

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter(Bakery.id == id).first()
    return make_response(bakery.to_dict())


@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_data = BakedGood.query.order_by(BakedGood.price.desc()).all()
    serialized_baked_goods = [baked_good.to_dict() for baked_good in baked_goods_data]
    return make_response(serialized_baked_goods)


@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).first()
    return make_response(most_expensive.to_dict())

if __name__ == '__main__':
    app.run(port=5555, debug=True)