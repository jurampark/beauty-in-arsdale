from app import db
import datetime

class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    sex = db.Column(db.String(1), nullable=False) # M || F
    user_age = db.Column(db.Integer, nullable=True)
    skin_type = db.Column(db.String(1), nullable=True)
    skin_color = db.Column(db.String(10), nullable=True) # ex. #FF080AAC

    def __init__(self, name=None, email=None, password=None, sex=None, user_age=None, skin_type=None, skin_color=None ):
        self.name = name
        self.email = email
        self.password = password
        self.sex = sex
        self.user_age = user_age
        self.skin_type = skin_type
        self.skin_color = skin_color

    def __repr__(self):
        return '<User %r>' % (self.name)

class Product(db.Model):

    __tablename__ = 'products'

    key = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String, unique=True, nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    product_type = db.Column(db.String(100) )
    product_desc = db.Column(db.String)
    product_big_img = db.Column(db.String(255))
    product_small_img = db.Column(db.String(255))
    video_review_url = db.Column(db.String(255))
    blog_review_list_id = db.Column(db.Integer) # is foreign key to blog_review
    product_brand = db.Column(db.String(255) )
    product_capacity = db.Column(db.Integer)
    product_price = db.Column(db.Integer)
    product_fit_for = db.Column(db.String(1), nullable=True) # like User's skin type
    product_color = db.Column(db.String(10) ) # 19ho || 18ho || ...
    product_color_rgb = db.Column(db.String(10), nullable=True) # ex. #FF080AAC
    # product_get_it_beauty_rank = db.Column(db.Integer)

    def __init__(self, product_name = None,product_id = None,product_type = None,product_desc = None,product_big_img = None,product_small_img = None,video_review_url = None, blog_review_list_id = None, product_brand = None,product_capacity = None,product_price = None,product_fit_for = None,product_color = None,product_color_rgb = None ):
        self.product_name = product_name
        self.product_id = product_id
        self.product_type = product_type
        self.product_desc = product_desc
        self.product_big_img = product_big_img
        self.product_small_img = product_small_img
        self.video_review_url = video_review_url
        self.blog_review_list_id = blog_review_list_id
        self.product_brand = product_brand
        self.product_capacity = product_capacity
        self.product_price = product_price
        self.product_fit_for = product_fit_for
        self.product_color = product_color
        self.product_color_rgb = product_color_rgb
        # self.product_get_it_beauty_rank = product_get_it_beauty_rank

    def __repr__(self):
        return '<Product %r>' % (self.product_name)

class BlogReview(db.Model):

    __tablename__ = 'blog_reviews'

    key = db.Column(db.Integer, primary_key=True)
    # blog_review_title = db.Column(db.String, nullable=True)
    # blog_review_type = db.Column(db.String, nullable=True)
    blog_product_key = db.Column(db.Integer)
    blog_review_writer = db.Column(db.String(255) )
    blog_review_date = db.Column(db.DateTime, default=datetime.datetime.now)
    blog_url = db.Column(db.String(255) )
    blog_summary = db.Column(db.String)
    blog_review_big_img = db.Column(db.String(255) )
    blog_review_small_img = db.Column(db.String(255) )

    def __init__(self, blog_product_key = None, blog_review_writer = None, blog_review_date = None, blog_url = None, blog_summary = None, blog_review_big_img = None, blog_review_small_img = None ):
        # self.blog_review_title = blog_review_title
        # self.blog_review_type = blog_review_type
        self.blog_product_key = blog_product_key
        self.blog_review_writer = blog_review_writer
        self.blog_review_date = blog_review_date
        self.blog_url = blog_url
        self.blog_summary = blog_summary
        self.blog_review_big_img = blog_review_big_img
        self.blog_review_small_img = blog_review_small_img

    def __repr__(self):
        return '<BlogReview %r>' % (self.blog_review_title)

class ProductSet(db.Model):
    __tablename__ = 'product_sets'

    key = db.Column(db.Integer, primary_key=True)
    set_name = db.Column(db.String(255) )
    set_category = db.Column(db.String(255) )
    set_product_count = db.Column(db.Integer)
    set_product_id_1 = db.Column(db.Integer)
    set_product_id_2 = db.Column(db.Integer)
    set_product_id_3 = db.Column(db.Integer)
    set_product_id_4 = db.Column(db.Integer)
    set_product_id_5 = db.Column(db.Integer)
    set_desc = db.Column(db.String)

    def __init__(self, set_name = None, set_category = None, set_product_count = None, set_product_id_1 = None, set_product_id_2 = None, set_product_id_3 = None, set_product_id_4 = None, set_product_id_5 = None, set_desc = None):
        self.set_name = set_name
        self.set_category = set_category
        self.set_product_count = set_product_count
        self.set_product_id_1 = set_product_id_1
        self.set_product_id_2 = set_product_id_2
        self.set_product_id_3 = set_product_id_3
        self.set_product_id_4 = set_product_id_4
        self.set_product_id_5 = set_product_id_5
        self.set_desc = set_desc

    def __repr__(self):
        return '<ProductSet %r>' % (self.set_name)
