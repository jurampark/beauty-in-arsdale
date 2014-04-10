# -*- coding: utf-8 -*-
from app import db
import datetime

# datetime field example
# created_on = db.Column(db.DateTime, default=db.func.now())
# updated_on = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
# creation_date = Column(DateTime, default=datetime.datetime.now())

# created at 20140327
class Users(db.Model):
    key = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    sex = db.Column(db.String(1))
    age = db.Column(db.Integer)
    skin_type = db.Column(db.String(100))
    skin_color = db.Column(db.String(10))
    created_time = db.Column(db.DateTime, default=db.func.now())

    interests = db.relationship('Interest', backref='user', lazy='dynamic')
    carts = db.relationship('Cart', backref='user', lazy='dynamic')

    def __init__(self, name, email, password, sex = None, age = None, skin_type = None, skin_color = None ):
        self.name = name
        self.email = email
        self.password = password
        self.sex = sex
        self.age = age
        self.skin_type = skin_type
        self.skin_color = skin_color

    def  __repr__(self):
        return '<Users %r>' % self.name

class Interest(db.Model):
    key = db.Column(db.Integer, primary_key=True)
    user_key = db.Column(db.Integer, db.ForeignKey('users.key'))
    product_key = db.Column(db.Integer, db.ForeignKey('product.key'))
    set_key = db.Column(db.Integer, db.ForeignKey('set.key'))
    is_set = db.Column(db.Boolean, default=False)
    created_time = db.Column(db.DateTime, default=db.func.now())

    __table_args__ = ( db.UniqueConstraint('user_key', 'product_key'), { } )

    def __init__(self, user_key, product_key, set_key, is_set ):
        self.user_key = user_key
        self.product_key = product_key
        self.set_key = set_key
        self.is_set = is_set

    def __repr__(self):
        return '<Interest %r>' % self.key

class Cart(db.Model):
    key = db.Column(db.Integer, primary_key=True)
    user_key = db.Column(db.Integer, db.ForeignKey('users.key'))
    product_key = db.Column(db.Integer, db.ForeignKey('product.key'))
    set_key = db.Column(db.Integer, db.ForeignKey('set.key'))
    is_set = db.Column(db.Boolean, default=False)
    created_time = db.Column(db.DateTime, default=db.func.now())

    def __init__(self, user_key, product_key, set_key, is_set ):
        self.user_key = user_key
        self.product_key = product_key
        self.set_key = set_key
        self.is_set = is_set

    def __repr__(self):
        return '<Cart %r>' % self.key

class Purchase(db.Model):
    key = db.Column(db.Integer, primary_key=True)
    user_key = db.Column(db.Integer, db.ForeignKey('users.key'))
    product_key = db.Column(db.Integer, db.ForeignKey('product.key'))
    set_key = db.Column(db.Integer, db.ForeignKey('set.key'))
    is_set = db.Column(db.Boolean, default=False)
    created_time = db.Column(db.DateTime, default=db.func.now())

    def __init__(self, user_key, product_key, set_key, is_set ):
        self.user_key = user_key
        self.product_key = product_key
        self.set_key = set_key
        self.is_set = is_set

    def __repr__(self):
        return '<Cart %r>' % self.key

class Product(db.Model):
    key = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category_key = db.Column(db.Integer, db.ForeignKey('category.key'))
    description = db.Column(db.Text)
    big_img_url = db.Column(db.String(255))
    small_img_url = db.Column(db.String(255))
    video_review_url = db.Column(db.String(255))
    brandname = db.Column(db.String(100))
    maker = db.Column(db.String(100))
    capacity = db.Column(db.String(100))
    price = db.Column(db.Integer)
    discount_rate = db.Column(db.Float, default=1, nullable=False)
    fit_skin_type = db.Column(db.String(100))
    color_description = db.Column(db.Text)
    color_rgb = db.Column(db.String(10))
    created_time = db.Column(db.DateTime, default=db.func.now())

    interests = db.relationship('Interest', backref='product', lazy='dynamic')
    carts = db.relationship('Cart', backref='product', lazy='dynamic')
    product_tags = db.relationship('ProductTag', backref='product', lazy='dynamic')
    blog_reviews = db.relationship('BlogReview', backref='product', lazy='dynamic')
    set_products = db.relationship('SetProduct', backref='product', lazy='dynamic')

    def __init__(self, name, category_key, description, big_img_url, small_img_url, video_review_url,
        brandname, maker, capacity, price, discount_rate, fit_skin_type, color_description, color_rgb ):
        self.name = name
        self.category_key = category_key
        self.description = description
        self.big_img_url = big_img_url
        self.small_img_url = small_img_url
        self.video_review_url = video_review_url
        self.brandname = brandname
        self.maker = maker
        self.capacity = capacity
        self.price = price
        self.discount_rate = discount_rate
        self.fit_skin_type = fit_skin_type
        self.color_description = color_description
        self.color_rgb = color_rgb

    def __repr__(self):
        return '<Product %s>' % self.name.encode("utf-8")
        

class ProductTag(db.Model):
    key = db.Column(db.Integer, primary_key=True)
    product_key = db.Column(db.Integer, db.ForeignKey('product.key'))
    tag_key = db.Column(db.Integer, db.ForeignKey('tag.key'))
    created_time = db.Column(db.DateTime, default=db.func.now())

    def __init__(self, product_key, tag_key ):
        self.product_key = product_key
        self.tag_key = tag_key

    def __repr__(self):
        return '<ProductTag %r>' % self.key

class Set(db.Model):
    key = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    big_img_url = db.Column(db.String(255))
    small_img_url = db.Column(db.String(255))
    discount_rate = db.Column(db.Float, default=1, nullable=False)
    category_key = db.Column(db.Integer, db.ForeignKey('category.key'))
    created_time = db.Column(db.DateTime, default=db.func.now())

    interests = db.relationship('Interest', backref='set', lazy='dynamic')
    set_products = db.relationship('SetProduct', backref='set', lazy='dynamic')

    def __init__(self, name, description, big_img_url, small_img_url, discount_rate, category_key):
        self.name = name
        self.description = description
        self.big_img_url = big_img_url
        self.small_img_url = small_img_url
        self.discount_rate = discount_rate
        self.category_key = category_key

    def __repr__(self):
        return '<Set %s>' % self.name.encode('utf-8')

class Category(db.Model):
    key = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    is_set = db.Column(db.Boolean, default=False)
    created_time = db.Column(db.DateTime, default=db.func.now())

    products = db.relationship('Product', backref='category', lazy='dynamic')
    sets = db.relationship('Set', backref='category', lazy='dynamic')

    def __init__(self, name, is_set):
        self.name = name
        self.is_set = is_set

    def __repr__(self):
        return '<Category %s>' % self.name.encode("utf-8")

class SetProduct(db.Model):
    key = db.Column(db.Integer, primary_key=True)
    set_key = db.Column(db.Integer, db.ForeignKey('set.key'))
    product_key = db.Column(db.Integer, db.ForeignKey('product.key'))
    created_time = db.Column(db.DateTime, default=db.func.now())

    def __init__(self, set_key, product_key):
        self.set_key = set_key
        self.product_key = product_key

    def __repr__(self):
        return '<SetProduct %r>' % self.key

class BlogReview(db.Model):
    key = db.Column(db.Integer, primary_key=True)
    product_key = db.Column(db.Integer, db.ForeignKey('product.key'))
    title = db.Column(db.String(100))
    writer = db.Column(db.String(100))
    review_created_time = db.Column(db.DateTime, default=db.func.now())
    url = db.Column(db.String(100))
    summary = db.Column(db.Text)
    big_img_url = db.Column(db.String(255))
    small_img_url = db.Column(db.String(255))
    created_time = db.Column(db.DateTime, default=db.func.now())

    def __init__(self, product_key, title, writer, review_created_time, url, summary, big_img_url, small_img_url):
        self.product_key = product_key
        self.title = title
        self.writer = writer
        self.review_created_time = review_created_time
        self.url = url
        self.summary = summary
        self.big_img_url = big_img_url
        self.small_img_url = small_img_url

    def __repr__(self):
        if self.title:
            return '<BlogReview %s>' % self.title.encode("utf-8")
        else:
            return '<BlogReview %s>' % self.writer.encode("utf-8")

class Tag(db.Model):
    key = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    created_time = db.Column(db.DateTime, default=db.func.now())

    product_tags = db.relationship('ProductTag', backref='tag', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Tag %s>' % self.name.encode("utf-8")
