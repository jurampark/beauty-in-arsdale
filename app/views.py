# -*- coding: utf-8 -*-
from app import app, db
from app.models import Users, Product, Interest, Cart, Category, Tag, BlogReview, SetProduct, Set
from flask import flash, redirect, render_template, request, session, url_for, g, jsonify
from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import func
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from werkzeug import generate_password_hash, check_password_hash
from functools import wraps

@app.route('/print_sample_module', methods = ['GET', 'POST'])
def printSampleModule():
    products = getProductListInInterest()

    return jsonify(
        success = True,
        data = {
            'usl': request.url,
            'baz': 'qux'
        }
    )

    # return request.form['testparam']

    # products = getProductList( None, 2)
    # print products

    # tags = getTagList( '수분')
    # print tags

    # sets = getSetList()
    # print sets

    # return 'good'

def getProduct( product_key ):
    # print g.db.session.query( Product, Category.name ).filter( Product.key == product_key ).filter( Product.category_key == Category.key )
    return_products = []
    products = g.db.session.query( Product, Category.name.label('category_name') ).filter( Product.key == product_key ).filter( Product.category_key == Category.key ).all()

    for product, category_name in products:
        product.category_name = category_name
        return_products.append( product )

    return return_products[0]

def getProductListInInterest():
    return_products = []
    query = g.db.session.query( Product, Category.name.label('category_name') ).\
    filter( Interest.product_key == Product.key ).\
    filter( Category.key == Product.category_key )
    if g.user:
        query = query.filter( Interest.user_key == g.user.key)

    products = query.all()

    for product, category_name in products:
        product.category_name = category_name
        return_products.append( product )

    return return_products;

def getProductListInCart():
    return_products = []
    query = g.db.session.query( Product, Category.name.label('category_name') ).\
    filter( Cart.product_key == Product.key ).\
    filter( Category.key == Product.category_key )
    if g.user:
        query = query.filter( Cart.user_key == g.user.key )

    products = query.all()

    for product, category_name in products:
        product.category_name = category_name
        return_products.append( product )

    return return_products

def getProductList( category_key = None, set_key = None ):
    if g.user:
        stmt = g.db.session.query( Interest ).filter( Interest.user_key == g.user.key ).subquery()
    else:
        stmt = g.db.session.query( Interest ).filter( Interest.user_key == -1 ).subquery()

    if set_key is not None:
        query = g.db.session.query( Product, Category.name.label('category_name'), stmt.c.key ).outerjoin( stmt, Product.key == stmt.c.product_key ).filter( and_( SetProduct.set_key == set_key, Product.key == SetProduct.product_key )).filter( Category.key == Product.category_key )
    else:
        query = g.db.session.query( Product, Category.name.label('category_name'), stmt.c.key ).outerjoin( stmt, Product.key == stmt.c.product_key ).filter( Category.key == Product.category_key )

    if category_key is not None:
        query = query.filter( Product.category_key == category_key )
    interestedProducts = query.all()
    products = []
    for product, category_name, isInterested in interestedProducts:
        product.category_name = category_name
        if isInterested == None:
            product.isInterested = False
        else:
            product.isInterested = True
        products.append( product )

    return products

def getProductListInTag( tag_key ):
    if g.user:
        stmt = g.db.session.query( Interest ).filter( Interest.user_key == g.user.key ).subquery()
    else:
        stmt = g.db.session.query( Interest ).filter( Interest.user_key == -1 ).subquery()

    query = g.db.session.query( Product, Category.name.label('category_name'), stmt.c.key ).outerjoin( stmt, Product.key == stmt.c.product_key ).filter( Category.key == Product.category_key )
    query = query.filter( and_(Product.key == ProductTag.product_key, ProductTag.tag_key == tag_key ) )
    interestedProducts = query.all()
    products = []
    for product, category_name, isInterested in interestedProducts:
        product.category_name = category_name
        if isInterested == None:
            product.isInterested = False
        else:
            product.isInterested = True
        products.append( product )

    return products

def getSetList( category_key = None ):
    if g.user:
        stmt = g.db.session.query( Interest ).filter( Interest.user_key == g.user.key ).subquery()
    else:
        stmt = g.db.session.query( Interest ).filter( Interest.user_key == -1 ).subquery()

    query = g.db.session.query( Set, stmt.c.key ).outerjoin( stmt, Set.key == stmt.c.set_key )
    if category_key is not None:
        query = query.filter( Set.category_key == category_key )

    interestedSets = query.all()
    sets = []
    for set_, isInterested in interestedSets:
        if isInterested == None:
            set_.isInterested = False
        else:
            set_.isInterested = True
        sets.append( set_ )

    return sets

def getCategoryList( is_set ):
    categorys = g.db.session.query( Category ).filter( Category.is_set == is_set ).all()
    return categorys

def getTagList( start_with_str = "" ):
    tags = g.db.session.query( Tag ).filter( Tag.name.like( start_with_str + '%' ) ).all()
    return tags

def getBlogReviewList( product_or_set_key, is_set = False ):
    if is_set is False:
        product_key = product_or_set_key
        blogReviews = g.db.session.query( BlogReview ).filter( BlogReview.product_key == product_key).all()
    else:
        set_key = product_or_set_key
        blogReviews = g.db.session.query( BlogReview ).filter( and_( SetProduct.set_key == set_key, BlogReview.product_key == SetProduct.product_key) ).all()

    return blogReviews

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
            return redirect( url_for('login', next = request.url) )
    return wrap


# sample code ----------------------------------------------------------------

def addProductOrSetToInterest( product_or_set_key, is_set ):
    if is_set:
        interest = Interest( g.user.key, None, product_or_set_key, True )
    else:
        interest = Interest( g.user.key, product_or_set_key, None, False )

    try:
        g.db.session.add( interest )
        g.db.session.commit()
        return True
    except IntegrityError:
        return False

def deleteProductOrSetInInterest( product_or_set_key, is_set ):
    if is_set:
        interest = g.db.session.query( Interest ).filter( Interest.set_key == product_or_set_key )
    else:
        interest = g.db.session.query( Interest ).filter( Interest.product_key == product_or_set_key )

    g.db.session.delete( interest )
    g.db.session.commit()

def addProductOrSetToCart( product_or_set_key, is_set ):
    if is_set:
        cart = Cart( g.user.key, None, product_or_set_key, True )
    else:
        cart = Cart( g.user.key, product_or_set_key, None, False )

    try:
        g.db.session.add( cart )
        g.db.session.commit()
        return True
    except IntegrityError:
        return False

def deleteProductOrSetInCart( product_or_set_key, is_set ):
    if is_set:
        cart = g.db.session.query( Cart ).filter( Cart.set_key == product_or_set_key )
    else:
        cart = g.db.session.query( Cart ).filter( Cart.product_key == product_or_set_key )

    g.db.session.delete( cart )
    g.db.session.commit()

# @app.route('/add_product_to_interest/<int:product_key>')
# @login_required
# def addProductToInterest( product_key ):
#     interest = Interest( g.user.key, product_key, None, False )
#     try:
#         g.db.session.add( interest )
#         g.db.session.commit()
#         return 'success'
#     except IntegrityError:
#         return 'fail'

# @app.route('/add_set_to_interest/<int:set_key>')
# @login_required
# def addSetToInterest( set_key ):
#     interest = Interest( g.user.key, None, set_key, True )
#     try:
#         g.db.session.add( interest )
#         g.db.session.commit()
#         return 'success'
#     except IntegrityError:
#         return 'fail'

# @app.route('/get_product_list')
# @app.route('/get_product_list/<int:category_key>')
# @login_required
# def sample_getProductList(category_key = None):

#     products = getProductListWithInterest( category_key )

#     for product in products:
#         print product, product.isInterested

#     return 'success'

# @app.route('/add_product_to_cart/<int:product_key>')
# @login_required
# def addProductToCart( product_key ):
#     cart = Cart( g.user.key, product_key, None, False )
#     try:
#         g.db.session.add( cart )
#         g.db.session.commit()
#         return 'success'
#     except IntegrityError:
#         return 'fail'

# @app.route('/add_set_to_cart/<int:set_key>')
# @login_required
# def addSetToCart( set_key ):
#     cart = Cart( g.user.key, None, set_key, True )
#     try:
#         g.db.session.add( cart )
#         g.db.session.commit()
#         return 'success'
#     except IntegrityError:
#         return 'fail'

# @app.route('/get_cart_product_list')
# @login_required
# def getCartProductList():
#     products = getProductListInCart()
#     print products

#     return 'success'

# --------------------------------------------------------------------------------

@app.route('/addProductToCart', methods = ['POST'])
def addProductCart():
    isSuccess = False
    message = None
    productKey = request.form['product_key']

    if g.user is None:
        message = 'login required'
    elif addProductOrSetToCart(productKey, False):
        isSuccess = True
        message = 'success'
    else :
        message = 'error'

    return jsonify(
        success = isSuccess,
        message = message
    )

@app.route('/addProductToInterest', methods = ['POST'])
def addProductInterest():
    isSuccess = False
    message = None
    productKey = request.form['product_key']

    if g.user is None:
        message = 'login required'
    elif addProductOrSetToInterest(productKey, False):
        isSuccess = True
        message = 'success'
    else :
        message = 'error'

    return jsonify(
        success = isSuccess,
        message = message
    )

@app.route('/delProductToInterest', methods = ['POST'])
def delProductCart():
    isSuccess = False
    message = None
    productKey = request.form['product_key']

    if g.user is None:
        message = 'login required'
    elif deleteProductOrSetInInterest(productKey, False):
        isSuccess = True
        message = 'success'
    else :
        message = 'error'

    return jsonify(
        success = isSuccess,
        message = message
    )

@app.route('/productdetailweb/<int:product_key>', methods = ['GET'])
def productDetailWeb(product_key):
    product = getProduct(product_key)
    blogList = getBlogReviewList(product_key, False)
    return render_template('product_detail_web.html', product=product, blogList=blogList)

@app.route('/')
def home():
    return redirect( url_for('index') )

@app.route('/login', methods=['GET', 'POST'] )
@app.route('/login/<path:next>', methods=['GET', 'POST'] )
def login( next = None ):
    if next is None:
        next = url_for('home')

    if g.user: # already login
        return redirect( next )

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
                return redirect( next )

    if error is not None:
        flash( error )
    return render_template( 'login.html', url_for_login_next = next )

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
    interests = getProductListInInterest();
    carts = getProductListInCart()
    return render_template('my_page.html', interests = interests, carts = carts)


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

@app.route('/productdetail/<int:product_key>', methods=['GET'])
###@login_required
def productDetail(product_key):
    product = getProduct(product_key)
    blogList = getBlogReviewList()
    return render_template('product_detail.html', product=product, blogList = blogList)

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
    carts = getProductListInCart()
    return render_template('cart.html', carts = carts)


@app.route('/index', methods = ['GET'])
def index():
    products = getProductList()
    return render_template('index.html', products = products)

@app.route('/indexweb', methods = ['GET'])
def indexweb():
    products = getProductList()
    return render_template('index_web.html', products = products)


@app.route('/mypageweb', methods = ['GET'])
@login_required
def mypageweb():
    interests = getProductListInInterest()
    return render_template('mypage_interesting_web.html', tabName='interesting', interests = interests)


@app.route('/purchaselist', methods = ['GET'])
@login_required
def purchaselist():
    carts = getProductListInCart()
    return render_template('mypage_purchase_web.html', tabName='purchase', carts = carts)


@app.route('/shopping1', methods = ['GET'])
def shoppingSet():
    products = None
    return render_template('shopping_set_web.html', products = products)

@app.route('/mshopping1', methods = ['GET'])
def mshoppingSet():
    products = g.db.session.query(Product).all()
    return render_template('shopping_set.html', products = products)

@app.route('/shopping2', methods = ['GET'])
def shoppingProduct():
    products = getProductList()
    return render_template('shopping_product_web.html', products = products)

@app.route('/mshopping2', methods = ['GET'])
def mshoppingProduct():
    products = getProductList()
    return render_template('shopping_product.html', products = products)

@app.route('/setdetail', methods = ['GET'])
def setDetail():
     ##product =g.db.session.query(Product).all()[0]
     return render_template('set_detail.html')

@app.route('/setdetailweb', methods = ['GET'])
def setDetailWeb():
     product =g.db.session.query(Product).all()[0]
     return render_template('set_detail_web.html', product= product)



