from app import app, db
from flask import flash, redirect, render_template, request, session, url_for
from functools import wraps
from app.forms import RegisterForm, LoginForm
from app.models import User
from sqlalchemy.exc import IntegrityError
from werkzeug import generate_password_hash, check_password_hash

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,error), 'error')

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

@app.route('/logout/')
def logout():
    session.pop('logged_in', None)
    session.pop('user_id', None)
    flash('You are logged out. Bye. :(')
    return redirect (url_for('login'))

@app.route('/')
@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method=='POST':
        u = User.query.filter_by(name=request.form['name']).first()
        if u is not None:
            passwordCheck = check_password_hash( u.password, request.form['password'] )

        if u is None or passwordCheck is False:
            error = 'Invalid username or password.'
        else:
            session['logged_in'] = True
            session['user_id'] = u.id
            flash('You are logged in. Go Crazy.')
            return redirect(url_for('members'))

    return render_template("login.html",
                           form = LoginForm(request.form),
                           error = error)

@app.route('/members/')
@login_required
def members():
    return render_template('members.html')

@app.route('/mockup', methods = ['GET', 'POST'])
def test():
    return 'register'

@app.route('/mypage/', methods=['GET'])
###@login_required
def myPage():
    return render_template('my_page.html')

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


@app.route('/register/', methods=['GET','POST'])
def register():
    error = None
    form = RegisterForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        new_user = User(
                    form.name.data,
                    form.email.data,
                    generate_password_hash(form.password.data),
                    )
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Thanks for registering. Please login.')
            return redirect(url_for('login'))
        except IntegrityError:
            error = 'Oh no! That username and/or email already exist. Please try again.'
    else:
        flash_errors(form)
    return render_template('register.html', form=form, error=error)

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
