from app import db

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
    product_type = db.Column(db.String(2) ) # BB || CC
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

    def __init__(self, product_name = None,product_id = None,product_type = None,product_desc = None,product_big_img = None,product_small_img = None,video_review_url = None, blog_review_list_id = None, product_brand = None,product_capacity = None,product_price = None,product_fit_for = None,product_color = None,product_color_rgb = None,product_get_it_beauty_rank = None ):
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

    def __repr__(self):
        return '<Product %r>' % (self.product_name)

class BlogReview(db.Model):

    __tablename__ = 'blog_reviews'

    key = db.Column(db.Integer, primary_key=True)
    blog_review_title = db.Column(db.String, nullable=True)
    blog_review_type = db.Column(db.String, nullable=True)
    blog_review_writer = db.Column(db.String(10) )
    blog_url = db.Column(db.String(255) )
    blog_summary = db.Column(db.String)
    blog_review_big_img = db.Column(db.String(255) )
    blog_review_small_img = db.Column(db.String(255) )

    def __init__(self, blog_review_title = None, blog_review_type = None, blog_review_writer = None, blog_url = None, blog_summary = None,product_small_img = None,video_review_url = None, blog_review_list_id = None, blog_review_big_img = None, blog_review_small_img = None ):
        self.blog_review_title = blog_review_title
        self.blog_review_type = blog_review_type
        self.blog_review_writer = blog_review_writer
        self.blog_url = blog_url
        self.blog_summary = blog_summary
        self.blog_review_big_img = blog_review_big_img
        self.blog_review_small_img = blog_review_small_img

    def __repr__(self):
        return '<BlogReview %r>' % (self.blog_review_title)