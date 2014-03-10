from app import db

class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    sex = db.Column(db.String(1), nullable=False)
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