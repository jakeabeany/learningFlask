from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin
from app import login

# UserMixin is a class that implements basic versions of the 4 required
# methods in Flask_Login:
# is_authenticated | is_active | is_anonymous | get_id
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)

    # not a database field - defines the link to Posts table
    posts = db.relationship("Post", backref="author", lazy="dynamic")

    # __repr__ is like toString
    def __repr__(self):
        return "<Username = {}, isAdmin = {}>".format(self.username, self.is_admin)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_admin(self):
        self.is_admin = True

    def set_not_admin(self):
        self.is_admin = False

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self):
        return "<Post {}>".format(self.body)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))