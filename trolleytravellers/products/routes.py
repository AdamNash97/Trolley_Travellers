from flask import Blueprint
from trolleytravellers.models import Product

orders = Blueprint('products', __name__)


@orders.route('/product', methods=['get'])
def get_products():
    products = Product.query.all()
    return jsonify({
        'success': True,
        'products': [product.info() for product in products]
    })

@orders.route('/product', methods=['POST'])
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

@orders.route('/product/<id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    if product is None:
        abort(404)
    product.delete()
    return jsonify({'success': True})

# PATCH - Used to create new data or update/modify existing data at the specified resource
@orders.route('/product', methods=['PATCH'])
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