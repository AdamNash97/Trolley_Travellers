from flask import Blueprint, jsonify, request, abort
from trolleytravellers import db
from trolleytravellers.models import Product, ProductSchema

products = Blueprint('products', __name__)

@products.route('/product_list', methods=['GET'])
def list_products():
    products = Product.query.all()
    product_schema = ProductSchema(many=True)
    output = product_schema.dump(products)
    return jsonify({'product' : output})
    
@products.route('/product/<id>', methods=['GET'])
def list_product(id):
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

@products.route('/add_multiple_products', methods=['POST'])
def new_products():
    try:
        jsonBody = request.get_json()
        for json_object in jsonBody:
            price_data = json_object.get('price')
            product_data = json_object.get('name')
            new_product = Product(price=price_data, name=product_data)
            db.session.add(new_product)
            db.session.commit()
            product_schema = ProductSchema()
            product_schema.jsonify(new_product)
        products = Product.query.all()
        product_schema = ProductSchema(many=True)
        output = product_schema.dump(products)
        return jsonify({'# products in database' : len(output)})
    except:
        abort(400)


@products.route('/update_product/<id>', methods=['PUT'])
def update_product(id):
    try:
        product = Product.query.get(id)
        price_data = request.json['price']
        product_data = request.json['name']
    
        product.price = price_data
        product.name = product_data
      
        db.session.commit()

        product_schema = ProductSchema()
        return product_schema.jsonify(product)
    except:
         abort(404)

@products.route('/delete_product/<id>', methods=['DELETE'])
def delete_product(id):
    try:
        product = Product.query.get(id)
        db.session.delete(product)
        db.session.commit()
        product_schema = ProductSchema()
        return product_schema.jsonify({product})
    except:
        abort(404)

