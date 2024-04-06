import math
from flask import render_template, request, redirect, jsonify, session
import dao
import utils
from saleapp import app, admin, login
from flask_login import login_user, logout_user
import cloudinary.uploader


@app.route('/')
def index():
    q = request.args.get('q')
    cate_id = request.args.get('category_id')
    page = request.args.get('page')

    products = dao.load_products(q=q, cate_id=cate_id, page=page)
    return render_template('index.html', products=products,
                           pages=math.ceil(dao.count_product()/app.config['PAGE_SIZE']))


@app.route('/products/<int:id>')
def details(id):
    product = dao.get_product_by_id(product_id=id)
    return render_template('product-details.html', product=product)


@app.route('/login', methods=['get', 'post'])
def login_my_user():
    err_msg = ''
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        user = dao.auth_user(username=username, password=password)
        if user:
            login_user(user)
            return redirect('/')
        else:
            err_msg = 'Username hoặc password sai!'

    return render_template('login.html', err_msg=err_msg)


@app.route('/logout', methods=['get'])
def logout_my_user():
    logout_user()
    return render_template('login.html')


@app.route("/admin-login", methods=['post'])
def process_admin_login():
    username = request.form.get('username')
    password = request.form.get('password')

    u = dao.auth_user(username=username, password=password)
    if u:
        login_user(user=u)

    return redirect('/admin')


@app.route("/register", methods=['get', 'post'])
def register_user():
    err_msg = None
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        confirm = request.form.get('confirm')

        if password.__eq__(confirm):
            avatar = request.files.get('avatar')
            if avatar:
                res = cloudinary.uploader.upload(avatar)
                avatar_path = res['secure_url']

            dao.register(name=request.form.get('name'),
                         avatar=avatar_path,
                         username=username,
                         password=password)
            return redirect('/login')
        else:
            err_msg = 'Mật khẩu không trùng khớp!'

    return render_template('register.html', err_msg=err_msg)


@app.route('/api/cart', methods=['post'])
def add_to_cart():
    cart = session.get('cart')

    if not cart:
        cart = {}

    id = str(request.json.get('id'))
    if id in cart:
        cart[id]["quantity"] += 1
    else:
        cart[id] = {
            "id": id,
            "name": request.json.get('name'),
            "price": request.json.get('price'),
            "quantity": 1
        }

    session['cart'] = cart

    return jsonify(utils.count_cart(cart))


@app.context_processor
def common_attributes():
    return {
        'categories': dao.load_categories()
    }


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True)
