from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

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

@app.route('/delete/<int:id>')
def delete(id):
    product_to_delete = Product.query.get_or_404(id)

    try:
        db.session.delete(product_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'Sorry, there was a problem deleting the product'

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    product_to_edit = Product.query.get_or_404(id)

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

if __name__ == "__main__":
    app.run(debug=True)
