from flask import Flask, render_template, url_for, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.inspection import inspect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Product %r>' % self.id


# Adding new product
# The user should specify all the parameters included in Product class,
# except id, which is generated automatically
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        product_name = request.form['name']
        product_description = request.form['description']
        product_type = request.form['type']
        product_price = request.form['price']
        product_quantity = request.form['quantity']

        new_product = Product(name=product_name,
                              description=product_description,
                              type=product_type,
                              price=product_price,
                              quantity=product_quantity)

        try:
            db.session.add(new_product)
            db.session.commit()
            return redirect('/')
        except:
            return 'Sorry, there was an issue adding your product'

    else:
        products = Product.query.all()
        return render_template('index.html', products=products)


# Removing selected product
@app.route('/delete/<product_id>')
def delete(product_id):
    product_to_delete = Product.query.get_or_404(product_id)

    try:
        db.session.delete(product_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'Sorry, there was a problem deleting the product'


# Adding one instance of a selected product (i.e. increasing quantity of a selected product by one)
@app.route('/add_one_item/<product_id>')
def add_one_item(product_id):
    product_to_add_one_item = Product.query.get_or_404(product_id)

    current_quantity = product_to_add_one_item.quantity
    product_to_add_one_item.quantity = current_quantity + 1

    try:
        db.session.commit()
        return redirect('/')
    except:
        return "Sorry, there was an issue adding an item"


# Removing one instance of a selected product (i.e. decreasing quantity of a selected product by one)
@app.route('/remove_one_item/<product_id>', methods=['GET', 'POST'])
def remove_one_item(product_id):
    product_to_remove_one_item = Product.query.get_or_404(product_id)
    current_quantity = product_to_remove_one_item.quantity

    if current_quantity >= 1:
        product_to_remove_one_item.quantity = current_quantity - 1
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "Sorry, there was an issue removing an item"
    else:
        return render_template('zero_quantity.html', product=product_to_remove_one_item)

# Going back to main page
@app.route('/to_main')
def to_main():
    products = Product.query.all()
    return render_template('index.html', products=products)

# Adding one instance of a selected product (i.e. increasing quantity of a selected product by one)
@app.route('/ship', methods=['GET', 'POST'])
def ship():
    if request.method == 'POST':
        address = request.form['address']
        id1 = int(request.form['id1'])
        id2 = int(request.form['id2'])
        id3 = int(request.form['id3'])
        id4 = int(request.form['id4'])
        id5 = int(request.form['id5'])
        quantity1 = int(request.form['quantity1'])
        quantity2 = int(request.form['quantity2'])
        quantity3 = int(request.form['quantity3'])
        quantity4 = int(request.form['quantity4'])
        quantity5 = int(request.form['quantity5'])
        ids = [id1, id2, id3, id4, id5]
        quantities = [quantity1, quantity2, quantity3, quantity4, quantity5]
        total_price = 0
        total_quantity = 0
        ready_to_ship = []
        products_available = Product.query.all()
        products_available_ids = set()
        for product in products_available:
            products_available_ids.add(product.id)
        print(products_available_ids)

        for shipment_item_id in range(0, 5):

            # That means that this field in shipment request was left blank
            if ids[shipment_item_id] == 0:
                pass

            # Checking if all the ids specified in the shipment request are available in the inventory
            elif ids[shipment_item_id] not in products_available_ids:
                return render_template('invalid_id.html', product_id=ids[shipment_item_id])
            else:

                product_to_ship = Product.query.get_or_404(ids[shipment_item_id])

                # Checking if each requested product has sufficient quantity
                if product_to_ship.quantity >= quantities[shipment_item_id]:
                    ready_to_ship.append(shipment_item_id)
                else:
                    return render_template('insufficient_quantity.html',
                                           product=product_to_ship,
                                           requested_quantity=quantities[shipment_item_id],
                                           quantity_in_stock=product_to_ship.quantity)

        # Itirating over the list of Shipment Request IDs that are ready to ship
        for shipment_item_id in ready_to_ship:
            product = Product.query.get_or_404(ids[shipment_item_id])
            current_quantity = product.quantity
            product.quantity = current_quantity - quantities[shipment_item_id]
            total_price += quantities[shipment_item_id]*product.price
            total_quantity += quantities[shipment_item_id]

        try:
            db.session.commit()
            return render_template('shipment_complete.html',
                                   total_price=total_price,
                                   total_quantity=total_quantity,
                                   address=address)
        except:
            return "Sorry, there was an issue saving your changes"

        try:
            db.session.commit()
            return redirect('/')
        except:
            return "Sorry, there was an issue adding an item"



# Editing selected product's information.
# It is possible to change all the parameters stored in Product class except id
@app.route('/edit/<product_id>', methods=['GET', 'POST'])
def edit(product_id):
    product_to_edit = Product.query.get_or_404(product_id)

    if request.method == 'POST':
        product_to_edit.name = request.form['name']
        product_to_edit.description = request.form['description']
        product_to_edit.type = request.form['type']
        product_to_edit.price = request.form['price']
        product_to_edit.quantity = request.form['quantity']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return "Sorry, there was an issue editing your product's information"

    else:
        return render_template('edit.html', product=product_to_edit)




# Error Handlers:

# Bad request
@app.errorhandler(400)
def bad_request(e):
    return jsonify('Bad request'), 400


# Page not found
@app.errorhandler(404)
def page_not_found(e):
    return jsonify('Cannot %s %s' % (request.method, request.path)), 404


# Method not allowed
@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify('%s method not allowed' % request.method), 405


# Too many requests
@app.errorhandler(429)
def too_many_requests(e):
    return jsonify('Too many requests'), 429


# Internal server error
@app.errorhandler(500)
def internal_server_error(e):
    return jsonify('Internal server error'), 500


if __name__ == "__main__":
    app.run(debug=True)

