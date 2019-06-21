from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.sql import func
from config import db, bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PW_REGEX = re.compile('^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$')
PHONE_REGEX=re.compile('^\d{3}\d{3}\d{4}$')


#make Users' model
class User(db.Model):
    __tablename__="users"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    city = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return '<User {}>'.format(self.first_name)

    #To validate if user enter correct information
    @classmethod
    def register_validation(cls, form):
        errors=[]
        if len(form['first_name']) < 1:
            errors.append('Please enter your first name!')
        if len(form['last_name']) < 1:
            errors.append('Please enter your last name!')
        if not EMAIL_REGEX.match(form['email']):
            errors.append("Please enter valid email address!")
        if len(form['phone']) < 9:
            errors.append("Please enter valid 10 digit phone number")
        if not PHONE_REGEX.match(form['phone']):
            errors.append("Please enter valid 10 digit phone number")
        
        if len(form['address']) < 1:
            errors.append ('Please enter your address')
        if len(form['state']) < 1:
            errors.append('Please enter your state')
        if len(form['city']) < 1:
            errors.append('Please enter your city')

    #validate if email is already registered
        existing_emails = cls.query.filter_by(email=form['email']).first()
        if existing_emails:
            errors.append("Email is already registered!")
        if form['password'] != form['confirm_password']:
            errors.append("Password must be match!")
        if len(form['password']) < 8:
            errors.append("Password must be at least 8 characters!")
        elif re.search('[0-9]', form['password']) is None:
            errors.append("Password required a number!")

        return errors
    
    #create users
    @classmethod
    def user_create(cls, form):
        pw_hash = bcrypt.generate_password_hash(form['password'])
        user = cls (
            first_name = form['first_name'],
            last_name = form['last_name'],
            email = form['email'],
            password = pw_hash,
            phone = form['phone'],
            address = form['address'],
            state = form['state'],
            city = form['city'],
        )

        db.session.add(user)
        db.session.commit()
        return user.id

    #validate login information
    @classmethod 
    def login_validation(cls, form):
        user = cls.query.filter_by(email=form['email']).first()
        print(user)
        if user:
            if bcrypt.check_password_hash(user.password, form['password']):
                return (True, user.id)
        return (False, "Email or password in incorrect")

    #edit user information 
    @classmethod
    def edit_user(cls, id, form):
        update_user = User.query.get(id)
        update_user.first_name = form['first_name']
        update_user.last_name = form['last_name']
        update_user.email = form['email']
        update_user.phone = form['phone']
        update_user.address = form['address']
        update_user.state = form['state']
        update_user.city = form['city']
        db.session.commit()
        print('user updated')
        return update_user.id

    #get users by id
    @classmethod
    def get_user(cls, user_id):
        user = User.query.get(id)
        print(user)
        return user

    #get all users
    #SELECT * FROM User
    @classmethod
    def get_all_user(cls):
        user = User.query.all()
        print(user)
        return user 


#make pizza table 


class Pizza(db.Model):
    __tablename__="pizzas"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    method = db.Column(db.String(255))
    size = db.Column(db.String(255))
    crust = db.Column(db.String(255))
    toppings = db.Column(db.String(255))
    qty = db.Column(db.Integer)
    user = db.relationship('User', foreign_keys=[user_id], backref=db.backref('users', cascade='all'))
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

    @classmethod
    def create_pizza(cls, form):
        pizza = cls (
            method = form['method'],
            size = form['size'],
            crust = form['crust'],
            qty = form['qty'],
        )
        db.session.add(pizza)
        db.session.commit()
        print ('pizza created')
        return pizza.id

    @classmethod 
    def get_user_pizza(cls, user_id):
        get_users_all_pizza = cls.query.filter_by(user_id = user_id).all()
        return get_users_all_pizza

    @classmethod
    def get_pizza(cls):
        get_pizza = cls.query.all()
        return get_pizza

    @classmethod
    def edit_pizza(cls, form, pizza_id):
        pizza_update = Pizza.get(pizza_id)
        pizza_update.method = form['method']
        pizza_update.size = form['size']
        pizza_update.crust = form['crust']
        pizza_update.toppings = form['qty']
        db.session.commit()
        return pizza_update
        
    @classmethod
    def delete(cls, pizza_id):
        delete_pizza = cls.query.get(pizza_id)
        db.session.delete(delete_pizza)
        db.session.commit()

class Topping(db.Model):
    __tablename__='toppings'
    id = db.Column(db.Integer, primary_key=True)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'), primay_key=True)
    pizza = db.relationship('Pizza', foreign_keys=[pizza_id], backref=db.backref('toppings', cascade='all'))
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())


        







      



