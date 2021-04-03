from flask import Blueprint
from trolleytravellers.models import Order

orders = Blueprint('orders', __name__)

@orders.route('/product', methods=['get'])
def get_product():
    products = Order.query.all()
    return jsonify({
        'success': True,
        'products': [product.short() for product in products]
    })

@orders.route('/product', methods=['POST'])
def new_product():
    try:
        jsonBody = request.get_json()
        id = jsonBody.get('id')
        price = jsonBody.get('price')
        quantity = jsonBody.get('quan')
        name = jsonBody.get('des')
        #image_link = jsonBody.get('picUrl')
        product = Order(id=id, price=price, quantity=quantity, name=name, image_link=image_link)
        product.insert()
        return jsonify({'success': True})
    except:
         abort(400)

@orders.route('/product/<id>', methods=['DELETE'])
def delete_product(id):
    product = Order.query.get(id)
    if product is None:
        abort(404)
    product.delete()
    return jsonify({'success': True})

@orders.route('/product', methods=['PATCH'])
def edit_product():
    try:
        jsonBody = request.get_json()
        id = jsonBody.get('id')
        product = Order.query.get(id)
        if product is None:
            abort(404)

        price = jsonBody.get('price')
        print(price)
        if price:
            product.price=price

        quantity = jsonBody.get('quan')
        if quantity:
            product.quantity=quantity

        name = jsonBody.get('des')
        if name:
            product.name=name

        image_link = jsonBody.get('picUrl')
        if image_link:
            product.image_link=image_link

        product.update()
        return jsonify({'success': True})
    except:
        abort(404)


    