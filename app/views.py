# -*- coding: utf-8 -*-
from app import app, db
from app.models import Users, Product, Interest, Cart, Category
from flask import flash, redirect, render_template, request, session, url_for, g
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import func
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from werkzeug import generate_password_hash, check_password_hash
from functools import wraps


def getProductListWhetherInterest( category_key ):
    stmt = g.db.session.query( Interest ).filter( Interest.user_key == g.user.key ).subquery()
    query = g.db.session.query( Product, stmt.c.key ).outerjoin( stmt, Product.key == stmt.c.product_key )
    if category_key is not None:
        query = query.filter( Product.category_key == category_key )
    interestedProducts = query.all()
    products = []
    for product, isInterested in interestedProducts:
        if isInterested == None:
            product.isInterested = False
        else:
            product.isInterested = True
        products.append( product )

    return products

def getProductListInCart():
    products = g.db.session.query( Product, Category.name ).\
    filter( Cart.product_key == Product.key ).\
    filter( Cart.user_key == g.user.key ).\
    filter( Category.key == Product.category_key ).all()
    return products

def getProductListInInterest():
    products = g.db.session.query( Product, Category.name ).\
    filter( Interest.product_key == Product.key ).\
    filter( Interest.user_key == g.user.key).\
    filter( Category.key == Product.category_key ).all()
    return products;

@app.before_request
def before_request():
    g.db = db
    g.user = None
    if 'user_key' in session:
        g.user = g.db.session.query(Users).filter(Users.key == session['user_key']).first()
        if g.user is None:
            session.pop('user_key', None )

@app.teardown_request
def teardown_request( exception ):
    pass

def login_required( func ):
    @wraps ( func )
    def wrap(*args, **kwargs ):
        if g.user:
            return func( *args, **kwargs )
        else:
            return redirect( url_for('login') )
    return wrap


# sample code ----------------------------------------------------------------

@app.route('/ttt')
@login_required
def ttt():
    products = getProductListInInterest()
    print products

    return 'success'

@app.route('/add_product_to_interest/<int:product_key>')
@login_required
def addProductToInterest( product_key ):
    interest = Interest( g.user.key, product_key, None, False )
    try:
        g.db.session.add( interest )
        g.db.session.commit()
        return 'success'
    except IntegrityError:
        return 'fail'

@app.route('/add_set_to_interest/<int:set_key>')
@login_required
def addSetToInterest( set_key ):
    interest = Interest( g.user.key, None, set_key, True )
    try:
        g.db.session.add( interest )
        g.db.session.commit()
        return 'success'
    except IntegrityError:
        return 'fail'

@app.route('/get_product_list')
@app.route('/get_product_list/<int:category_key>')
@login_required
def getProductList(category_key = None):

    products = getProductListWithInterest( category_key )

    for product in products:
        print product, product.isInterested

    return 'success'

@app.route('/get_interest_product_list')
@login_required
def getInterestProductList():
    interests = g.user.interests.all()
    for interest in interests:
        print interest.product

    return 'success'

@app.route('/add_product_to_cart/<int:product_key>')
@login_required
def addProductToCart( product_key ):
    cart = Cart( g.user.key, product_key, None, False )
    try:
        g.db.session.add( cart )
        g.db.session.commit()
        return 'success'
    except IntegrityError:
        return 'fail'

@app.route('/add_set_to_cart/<int:set_key>')
@login_required
def addSetToCart( set_key ):
    cart = Cart( g.user.key, None, set_key, True )
    try:
        g.db.session.add( cart )
        g.db.session.commit()
        return 'success'
    except IntegrityError:
        return 'fail'

@app.route('/get_cart_product_list')
@login_required
def getCartProductList():
    products = getProductListInCart()
    print products

    return 'success'

@app.route('/get_category_list')
@app.route('/get_category_list/<isSet>')
def getCategoryList( isSet = False ):
    if isSet is not False:
        isSet = True

    categorys = g.db.session.query( Category ).filter( Category.is_set == isSet ).all()

    for category in categorys:
        print category

    return 'success'

# --------------------------------------------------------------------------------



@app.route('/productdetailweb', methods = ['GET'])
def productDetailWeb():
    products =g.db.session.query(Product).all()[0:5]
    product = products[0]
    return render_template('product_detail_web.html', products=products, product = product)

@app.route('/')
def home():
    return redirect( url_for('myPage') )

@app.route('/login', methods=['GET', 'POST'] )
def login():
    if g.user: # already login
        return redirect( url_for('home') )

    error = None

    if request.method == 'POST':
        # get post params
        email = request.form.get('email')
        password = request.form.get('password')

        user = g.db.session.query( Users ).filter(Users.email == email ).first()
        if user is None:
            error = 'fail_invalid_email'
        else:
            if not check_password_hash( user.password, password ):
                error = 'fail_invalid_password'
            else:
                session['user_key'] = user.key
                return redirect( url_for('home' ) )

    if error is not None:
        flash( error )
    return render_template( 'login.html' )

@app.route('/logout')
def logout():
    session.pop('user_key', None )
    return redirect( url_for('home') )

@app.route('/register', methods=['GET', 'POST'] )
def register():
    if g.user: # already login
        return redirect( url_for('home') )

    error = None

    if request.method == 'POST':
        #get post params
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        sex = request.form.get('sex')

        error = validate_register( name, email, password, sex )
        if error is None:
            new_user = Users( name, email, generate_password_hash(password), sex, )
            try:
                g.db.session.add( new_user )
                g.db.session.commit()
                return redirect( url_for('home') )
            except IntegrityError:
                error = 'fail_register'

    return render_template( 'register.html' )


@app.route('/product_sample')
def product_sample():
    products = g.db.session.query(Product).all()

    return render_template( 'product_sample.html', products = products )

@app.route('/product/<int:product_key>')
def product_detail(product_key):
    product = g.db.session.query(Product).filter(Product.key == product_key ).first()
    return product.product_name


# should return error if exist
def validate_register( name, email, password, sex ):
    return None

@app.route('/mypage')
@login_required
def myPage():
    products = g.db.session.query(Product).all()
    return render_template('my_page.html', products = products)


@app.route('/update_user_profile', methods=['GET', 'POST'])
@login_required
def updateUserProfile():

    if request.method == 'POST':
        # get post params
        g.user.age = request.form.get('age')
        g.user.sex = request.form.get('sex')
        g.user.skin_type = request.form.get('skin_type')
        g.user.skin_color = request.form.get('skin_color')

        g.db.session.commit()

        return redirect( url_for('home') )

    return render_template('update_user_profile.html')







def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,error), 'error')


@app.route('/members/')
@login_required
def members():
    return render_template('members.html')

@app.route('/mockup', methods = ['GET', 'POST'])
def test():
    return 'register'

@app.route('/join/', methods=['GET'])
###@login_required
def join():
    return render_template('join.html')

@app.route('/productdetail/', methods=['GET'])
###@login_required
def productDetail():
    return render_template('product_detail.html')

@app.route('/blogdetail/', methods=['GET'])
###@login_required
def blogDetail():
    return render_template('blog_detail.html')

@app.route('/comparablelist/', methods=['GET'])
###@login_required
def comparableList():
    return render_template('comparable_list.html')

@app.route('/comparabledetaillist/', methods=['GET'])
###@login_required
def comparableDetailList():
    return render_template('comparable_detail_list.html')

@app.route('/loginbyfacebook/')
def loginbyfacebook():
    return render_template('fb_login.html')

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

@app.errorhandler(404)
def internal_error(error):
    return render_template('404.html'), 404



@app.route('/cart', methods = ['GET'])
def cart():
    return render_template('cart.html')


@app.route('/index', methods = ['GET'])
def index():
    products = g.db.session.query(Product).all()
    return render_template('index.html', products = products)

@app.route('/indexweb', methods = ['GET'])
def indexweb():
    products = g.db.session.query(Product).all()
    return render_template('index_web.html', products = products)


@app.route('/mypageweb', methods = ['GET'])
@login_required
def mypageweb():
    products = g.db.session.query(Product, Category.name).filter( Product.category_key == Category.key ).all()
    return render_template('mypage_interesting_web.html', tabName='interesting', products=products[0:7])


@app.route('/purchaselist', methods = ['GET'])
@login_required
def purchaselist():
    products = g.db.session.query(Product).all()
    return render_template('mypage_purchase_web.html', tabName='purchase', products = products[0:4])


@app.route('/shopping1', methods = ['GET'])
def shoppingSet():
    products = g.db.session.query(Product).all()
    return render_template('shopping_set_web.html', products = products)

@app.route('/mshopping1', methods = ['GET'])
def mshoppingSet():
    products = g.db.session.query(Product).all()
    return render_template('shopping_set.html', products = products)

@app.route('/shopping2', methods = ['GET'])
def shoppingProduct():
    products = g.db.session.query(Product).all()
    return render_template('shopping_product_web.html', products = products)

@app.route('/mshopping2', methods = ['GET'])
def mshoppingProduct():
    products = g.db.session.query(Product).all()
    return render_template('shopping_product.html', products = products)

@app.route('/setdetail', methods = ['GET'])
def setDetail():
     ##product =g.db.session.query(Product).all()[0]
     return render_template('set_detail.html')




