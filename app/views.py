from app import app, db
from app.models import User
from flask import flash, redirect, render_template, request, session, url_for, g
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from werkzeug import generate_password_hash, check_password_hash
from functools import wraps

@app.before_request
def before_request():
    g.db = db
    g.user = None
    if 'user_id' in session:
        g.user = g.db.session.query(User).filter(User.id == session['user_id']).first()
        if g.user is None:
            session.pop('user_id', None )

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

        user = g.db.session.query( User ).filter(User.email == email ).first()
        if user is None:
            error = 'fail_invalid_email'
        else:
            if not check_password_hash( user.password, password ):
                error = 'fail_invalid_password'
            else:
                session['user_id'] = user.id
                return redirect( url_for('home' ) )

    if error is not None:
        flash( error )
    return render_template( 'login.html' )

@app.route('/logout')
def logout():
    session.pop('user_id', None )
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
            new_user = User( name, email, generate_password_hash(password), sex, )
            try:
                g.db.session.add( new_user )
                g.db.session.commit()
                return redirect( url_for('home') )
            except IntegrityError:
                error = 'fail_register'

    return render_template( 'register.html' )

# should return error if exist
def validate_register( name, email, password, sex ):
    return None

@app.route('/mypage')
@login_required
def myPage():
    return render_template('my_page.html')










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

@app.route('/convertprofile/', methods=['GET'])
###@login_required
def convertProfile():
    return render_template('insert_profile_info.html')

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