from saleapp.models import Category, Product, User, Receipt, ReceiptDetails, Comment
from saleapp import app, db
import hashlib
from flask_login import current_user
from sqlalchemy import func
from datetime import datetime


def load_categories():
    return Category.query.all()
    # with open('data/categories.json', encoding='utf-8') as f:
    #     return json.load(f)


def count_product():
    return Product.query.count()


def load_products(q=None, cate_id=None, page=None):
    query = Product.query

    if q:
        query = query.filter(Product.name.contains(q))

    if cate_id:
        query = query.filter(Product.category_id.__eq__(cate_id))

    if page:
        page_size = app.config['PAGE_SIZE']
        start = (int(page) - 1) * page_size
        query = query.slice(start, start + page_size)

    return query.all()
    # with open('data/products.json', encoding='utf-8') as f:
    #     products = json.load(f)
    #
    #     if q:
    #         products = [p for p in products if p['name'].find(q) >= 0]
    #
    #     if cate_id:
    #         products = [p for p in products if p['category_id'].__eq__(int(cate_id))]
    #
    #     return products


def get_product_by_id(product_id):
    return Product.query.get(product_id)
    # with open('data/products.json', encoding='utf-8') as f:
    #     products = json.load(f)
    #     for p in products:
    #         if p['id'] == product_id:
    #             return p


def get_user_by_id(id):
    return User.query.get(id)


def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password)).first()


def add_user(name, username, password, avatar):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = User(name=name, username=username, password=password, avatar=avatar)
    db.session.add(u)
    db.session.commit()


def add_receipt(cart):
    if cart:
        r = Receipt(user=current_user)
        db.session.add(r)

        for c in cart.values():
            d = ReceiptDetails(quantity=c['quantity'], unit_price=c['price'],
                               receipt=r, product_id=c['id'])
            db.session.add(d)

        db.session.commit()


def count_products_by_cate():
    return db.session.query(Category.id, Category.name, func.count(Product.id))\
        .join(Product, Product.category_id.__eq__(Category.id), isouter=True)\
        .group_by(Category.id).all()


def stats_revenue_by_product(kw=None):
    query = db.session.query(Product.id, Product.name, func.sum(ReceiptDetails.quantity*ReceiptDetails.unit_price))\
        .join(ReceiptDetails, ReceiptDetails.product_id.__eq__(Product.id), isouter=True)

    if kw:
        query = query.filter(Product.name.contains(kw))

    return query.group_by(Product.id).all()


def stats_revenue_by_period(year=datetime.now().year, period='month'):
    query = db.session.query(func.extract(period, Receipt.created_date),
                             func.sum(ReceiptDetails.quantity*ReceiptDetails.unit_price))\
        .join(ReceiptDetails, ReceiptDetails.receipt_id.__eq__(Receipt.id))\
        .filter(func.extract('year', Receipt.created_date).__eq__(year))

    return query.group_by(func.extract(period, Receipt.created_date))\
        .order_by(func.extract(period, Receipt.created_date)).all()


def get_comment(product_id):
    return Comment.query.filter(Comment.product_id.__eq__(product_id)).order_by(-Comment.id)


def add_comment(product_id, content):
    c = Comment(product_id=product_id, content=content, user_id=current_user.id)
    db.session.add(c)
    db.session.commit()

    return c


if __name__ == '__main__':
    print(load_categories())