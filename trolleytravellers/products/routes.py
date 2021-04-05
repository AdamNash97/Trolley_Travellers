from flask import Blueprint, jsonify
from trolleytravellers.models import Product, ProductSchema

products = Blueprint('products', __name__)

@products.route('/product_list', methods=['GET'])
def list_products():
    products = Product.query.all()
    product_schema = ProductSchema(many=True)
    output = product_schema.dump(products)
    return jsonify({'product' : output})
    
@products.route('/product/<id>', methods=['GET'])
def list_product():
    try:
        product = Product.query.get(id)
        product_schema = ProductSchema()
        return product_schema.jsonify(product)
    except:
         abort(400)

@products.route('/add_product', methods=['POST'])
def new_product():
    try:
        price_data = request.json['price']
        product_data = request.json['name']
        new_product = Product(price=price_data, name=product_data)
        db.session.add(new_product)
        db.session.commit()
        product_schema = ProductSchema()
        return product_schema.jsonify(new_product)
    except:
         abort(400)