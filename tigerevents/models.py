from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from tigerevents import db, login_manager
from flask import current_app
from flask_login import UserMixin



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# class models
class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    # many to many relationships
    maybe_e = db.relationship("Event", secondary="cart")
    going_e = db.relationship("Event", secondary="orders")

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.email}')"


class Event(db.Model):
    __tablename__= "events"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    description = db.Column(db.Text, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default_campaign.jpg")
    
    maybe_u = db.relationship("User", secondary="cart")
    going_u = db.relationship("User", secondary="orders")

    def __repr__(self):
        return f"Campaign('{self.title}', '{self.date_posted}', '{self.goal}')"


# association tables for events and users
class Order(db.Model):
    __tablename__="orders"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    dttm = db.Column(db.DateTime,, nullable=False, default=datetime.utcnow)

    user = db.relationship(User, backref=backref("orders", cascade="all, delete-orphan"))
    event = db.relationship(Event, backref=backref("orders", cascade="all, delete-orphan"))


class Cart(db.Model):
    __tablename__= "cart"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    dttm = db.Column(db.DateTime,, nullable=False, default=datetime.utcnow)

    user = db.relationship(User, backref=backref("cart", cascade="all, delete-orphan"))
    event = db.relationship(Event, backref=backref("cart", cascade="all, delete-orphan"))
    




    

