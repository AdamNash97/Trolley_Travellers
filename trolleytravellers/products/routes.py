from flask import Blueprint, jsonify
from trolleytravellers.models import Product, ProductSchema

products = Blueprint('products', __name__)

@products.route('/product_list', methods=['GET'])
def list_products():
    products = Product.query.all()
    product_schema = ProductSchema(many=True)
    output = product_schema.dump(products)
    return jsonify({'product' : output})
    
@products.route('/product', methods=['POST'])
def new_product():
    try:
        jsonBody = request.get_json()
        id = jsonBody.get('id')
        price = jsonBody.get('price')
        quantity = jsonBody.get('quantity')
        name = jsonBody.get('name')
        #image_link = jsonBody.get('picUrl')
        product = Product(id=id, price=price, name=name, quantity=quantity)
        product.insert()
        return jsonify({'success': True})
    except:
         abort(400)

@products.route('/product/<id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    if product is None:
        abort(404)
    product.delete()
    return jsonify({'success': True})

# PATCH - Used to create new data or update/modify existing data at the specified resource
@products.route('/product', methods=['PATCH'])
def edit_product():
    try:
        jsonBody = request.get_json()
        id = jsonBody.get('id')
        product = Product.query.get(id)
        if product is None:
            abort(404)

        price = jsonBody.get('price')
        print(price)
        if price:
            product.price=price

            name = jsonBody.get('des')
        if name:
            product.name=name

        quantity = jsonBody.get('quantity')
        if quantity:
            product.quantity=quantity

        product.update()
        return jsonify({'success': True})
    except:
        abort(404)