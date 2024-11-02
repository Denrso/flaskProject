from flask import render_template, redirect, url_for, flash, jsonify, session, request
from flask_login import login_user, current_user, logout_user, login_required
from app import app, db
from models import User, Product, UserRole
from forms import RegistrationForm, LoginForm, ProductForm,DeleteForm

import yoomoney

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')




@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        role = UserRole.query.filter_by(name='User').first()
        user = User(username=form.username.data, email=form.email.data, password=form.password.data, role=role)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/products', methods=['GET', 'POST'])
@login_required
def products():
    products = Product.query.all()

    return render_template('products.html', title='Products', products=products)



@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if current_user.role.name not in ['Admin', 'Manager']:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('home'))

    form = ProductForm()
    if form.validate_on_submit():
        product = Product(name=form.name.data, price=form.price.data, description=form.description.data)
        db.session.add(product)
        db.session.commit()
        flash('Product has been added!', 'success')
        return redirect(url_for('admin'))

    products = Product.query.all()
    delete_form = DeleteForm()
    return render_template('admin.html', title='Admin', form=form, products=products, delete_form=delete_form)

# Маршрут для удаления продукта



@app.route('/delete_product/<int:product_id>', methods=['POST'])
@login_required
def delete_product(product_id):

    form = DeleteForm()
    product = Product.query.get_or_404(product_id)

    if current_user.role.name not in ['Admin', 'Manager']:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('home'))

    if form.validate_on_submit():
        db.session.delete(product)
        db.session.commit()
        flash('Продукт успешно удален', 'success')
        return redirect(url_for('products'))
    else:
        flash('Ошибка при удалении продукта', 'danger')
        return redirect(url_for('products'))

@app.route('/cart/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    # Логика добавления товара в корзину
    # если корзина ещё не создана
    if not session.get('cart'):
        session['cart'] = []

    # добавляем инфу о товаре в список
    session['cart'] += [{
        'product_name': product_id,
    }]

    flash(f'Product {product_id} has been added to your cart!', 'success')
    return jsonify(success=True)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/createdb')
def tables():
    db.create_all()
    roles = ['User', 'Admin', 'Manager']
    for role in roles:
        if not UserRole.query.filter_by(name=role).first():
            new_role = UserRole(name=role)
            db.session.add(new_role)
    db.session.commit()
    return True
# yoo_money_api = yoomoney.YooMoneyAPI(token='YOUR_YOOMONEY_API_TOKEN')


# @app.route('/pay', methods=['POST'])
# @login_required
# def pay():
#     amount = request.json.get('amount')
#     description = "Payment for order"
#
#     payment = yoo_money_api.payment.create(amount, '643', description)
#     if payment:
#         return jsonify({'success': True, 'url': payment.confirmation.confirmation_url})
#     return jsonify({'success': False, 'error': 'Payment creation failed'})
