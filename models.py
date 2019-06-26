from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.sql import func
from config import db, bcrypt
import re
import random

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PW_REGEX = re.compile('^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$')
PHONE_REGEX=re.compile('^\d{3}\d{3}\d{4}$')


#make Users' table 
class User(db.Model):
    __tablename__="users"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())


    #To validate if user enter correct information
    @classmethod
    def register_validation(cls, form):
        print(form)
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
        if len(form['state']) < 1:
            errors.append('Please enter your state')
        if len(form['city']) < 1:
            errors.append('Please enter your city')

    #validate if email is already registered
        existing_emails = cls.query.filter_by(email=form['email']).first()
        if existing_emails:
            errors.append("Email is already registered!")

     #check if password and confirm password match 
        if form['password'] != form['confirm_password']:
            errors.append("Password must be match!")

    #validate password must be at least 8 character
        if len(form['password']) < 8:
            errors.append("Password must be at least 8 characters!")

    #validate password must has a number between 0-9
        elif re.search('[0-9]', form['password']) is None:
            errors.append("Password required a number!")
        
        # if not PW_REGEX.match(form['password']):
        #     errors.append("Paasword must have a number, a special character, upper and lowercase!")

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
        )
        db.session.add(user)
        db.session.commit()
        address = Address.new(user.id, form)
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
        address = update_user.addresses[0]
        address.street = form['street']
        address.city = form['city']
        address.state = form['state']
        address.zip_code = form['zip_code']
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
class Address(db.Model):
    __tablename__='addresses'
    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(255))
    city = db.Column(db.String(255))
    state = db.Column(db.String(255))
    zip_code = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

    #One User can have many Address
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', foreign_keys=[user_id], backref=db.backref('addresses', cascade='all'))

    @classmethod
    def new(cls, user_id, form):
        address = cls (
            user_id = user_id,
            street = form['street'],
            city = form['city'],
            state = form['state'],
            zip_code = form['zip_code'],
        )
        db.session.add(address)
        db.session.commit()
        return address.id



# class Order(db.Model):
#     __tablename__='orders'
#     id = db.Column(db.Integer, primary_key=True)
#     method = db.Column(db.String(255))
#     size = db.Column(db.String(255))
#     crust = db.Column(db.String(255))
#     qty = db.Column(db.Integer)
#     price = db.Column(db.Float)
#     created_at = db.Column(db.DateTime, server_default=func.now())
#     updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

#     #User can have many orders
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
#     user = db.relationship('User', foreign_keys=[user_id], backref=db.backref('orders', cascade='all'))
#     #

#     @classmethod
#     def create_order(cls, form):
#         order = cls (
#             method = form['method'],
#             size = form['size'],
#             crust = form['crust'],
#             qty = form['qty'],
#             price = form['price'],
#         )
#         db.session.add(order)
#         db.session.commit()
#         print (order)
#         return order.id

#     @classmethod 
#     def get_user_order(cls, user_id):
#         get_users_all_order = cls.query.filter_by(user_id = user_id).all()
#         return get_users_all_order

#     @classmethod
#     def get_order(cls):
#         get_order = cls.query.all()
#         return get_order

#     @classmethod
#     def edit_order(cls, form, order_id):
#         order_update = Order.get(order_id)
#         order_update.method = form['method']
#         order_update.size = form['size']
#         order_update.crust = form['crust']
#         order_update.toppings = form['qty']
#         db.session.commit()
#         return order_update
        
#     @classmethod
#     def delete(cls, order_id):
#         delete_order = cls.query.get(order_id)
#         db.session.delete(delete_order)
#         db.session.commit()
class Order(db.Model):
    __tablename__='orders'
    id = db.Column(db.Integer, primary_key=True)
    subtotal = db.Column(db.Float)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    #user can have many orders
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', foreign_keys=[user_id], backref=db.backref('orders'), cascade='all')

    # @classmethod 
    # def new_order(cls, order_id):
    #     order = Order.query.get(order.id)
    #     new_orders = cls (
    #         user_id = order.user_id,
    #     )
    #     db.session.add(new_orders)
    #     db.session.commit()
    #     for pizza in Pizza:
    #         new_pizza = Pizza(
    #             order_id = new_orders.id,
    #             size_id = pizza.size_id,
    #             crust_id = pizza.crust_id,
    #             qty = pizza.qty,
    #             method_id = pizza.method_id,
    #             )
    #         db.session.add(new_pizza)
    #         db.session.commit()
    #         for topping in pizza.toppings:
    #             new_topping = Topping(
    #                 pizza_id = new_pizza.id,
    #                 toppings_menu_id = topping.toppings.menu_id
    #                 )
    #             db.session.add(new_topping)
    #             db.session.commit()
    #     return new_orders
            
    @classmethod
    def get_order(cls):
        get_order = cls.query.all()
        return get_order

    @classmethod
    def get_pizza_orders(cls):
        pizza = Pizza.query.all()
        return pizza


class Pizza(db.Model):
    __tablename__ = 'pizzas'
    id = db.Column(db.Integer, primary_key=True)
    qty = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate = func.now())

    #Order can have many pizza ?
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    order = db.relationship('Order', foreign_keys=[order_id], backref=db.backref('pizzas'), cascade='all')

    #Method can have many pizza?
    method_id = db.Column(db.Integer, db.ForeignKey('methods.id'))
    method = db.relationship('Method', foreign_keys=[method_id], backref=db.backref('pizzas'), cascade='all')

    #Crust can have many pizza?
    crust_id = db.Column(db.Integer, db.ForeignKey('crusts.id'))
    crust = db.relationship('Crust', foreign_keys=[crust_id], backref=db.backref('pizzas'), cascade='all')

    #Size can have many pizza?
    size_id = db.Column(db.Integer, db.ForeignKey('sizes.id'))
    size = db.relationship('Size', foreign_keys=[size_id], backref=db.backref('pizzas'), cascade='all')


    @classmethod
    def create_pizza(cls, order_id, form):
        size_id = form['size']
        crust_id = form['crust']
        method_id = form['method']
        qty = form['qty']
        create_pizza = cls (
            order_id = order_id,
            size_id = size_id,
            crust_id = crust_id,
            method_id = method_id,
            qty = qty,
        )
        db.session.add(create_pizza)
        db.session.commit()
        for topping in topping_ids:
            topping = Topping.create_pizzas(create_pizza.id, topping.id)
        
        return create_pizza.id

    @classmethod 
    def get_user_order(cls, order_id):
        get_users_all_order = cls.query.filter_by(order_id = order_id).all()
        return get_users_all_order

#size table #small, large, medium
class Size(db.Model):
    __tablename__ = 'sizes'
    id = db.Column(db.Integer, primary_key=True)
    size = db.Column(db.String(255))
    price = db.Column(db.Float)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

    @classmethod
    def create_size(cls, form):
        size = cls (
            size = form['size'],
            price = form['price'],
        )
        db.session.add(size)
        db.session.commit()
        return size.id

    @classmethod
    def get_all_size(cls):
        get_size = cls.query.all()
        return get_size


#crust table #thin or thick
class Crust(db.Model):
    __tablename__ = 'crusts'
    id = db.Column(db.Integer, primary_key=True)
    crust = db.Column(db.String(255))
    price = db.Column(db.Float)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

    @classmethod
    def create_crust(cls, form):
        crust = cls (
            crust = form['crust'],
            price = form['price'],
        )
        db.session.add(crust)
        db.session.commit()
        return crust.id

    @classmethod
    def get_all_crust(cls):
        get_crusts = cls.query.all()
        return get_crusts

#methods table #pickup or delievery
class Method(db.Model):
    __tablename__ = 'methods'
    id = db.Column(db.Integer, primary_key=True)
    method = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

    @classmethod
    def create_method(cls, form):
        method = cls (
            method = form['method'],
        )
        db.session.add(method)
        db.session.commit()
        return method.id

    @classmethod
    def get_all_methods(cls):
        get_methods = cls.query.all()
        return get_methods


class Topping_Menu(db.Model):
    __tablename__ = 'toppings_menu'
    id = db.Column(db.Integer, primary_key=True)
    topping = db.Column(db.String(255))
    price = db.Column(db.Float)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

    @classmethod
    def new(cls, form):
        add_topping = cls (
            topping = form['topping'],
            price = form['price'],
        )
        db.session.add(add_topping)
        db.session.commit()
        return add_topping.id

    @classmethod
    def get_all_toppings(cls):
        get_all_topping = cls.query.all()
        return get_all_topping

class Topping(db.Model):
    __tablename__ = 'toppings'
    id = db.Column(db.Integer, primary_key=True)

    #Pizza can have many topping
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'))
    pizza = db.relationship('Pizza', foreign_keys=[pizza_id], backref=db.backref('toppings'), cascade='all')

    #topping menu can have many toppings
    topping_menu_id = db.Column(db.Integer, db.ForeignKey('toppings_menu.id'))
    topping_menu = db.relationship('Topping_Menu', foreign_keys=[topping_menu_id], backref=db.backref('toppings'), cascade='all')

    @classmethod
    def create_pizzas(cls, pizza_id, toppings_menu_id):
        create_pizza = cls (
            pizza_id = pizza_id,
            toppings_menu_id = toppings_menu_id
        )
        db.session.add(create_pizza)
        db.session.commit()

# class Topping(db.Model):
#     __tablename__='toppings'
#     id = db.Column(db.Integer, primary_key=True)
#     order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
#     topping = db.Column(db.String(255))
#     order = db.relationship('Order', foreign_keys=[order_id], backref=db.backref('toppings', cascade='all'))
#     created_at = db.Column(db.DateTime, server_default=func.now())
#     updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

#     @classmethod
#     def new(cls, form):
#         new_toppings = cls (
#             topping = form['topping'],
#         )
#         db.session.add(new_toppings)
#         db.session.commit()
#         return new_toppings

#     @classmethod
#     def delete(cls, topping):
#         db.session.delete(topping)
#         db.session.commit()

#     @classmethod
#     def get_all(cls):
#         get_all_toppings = cls.query.all()
#         return get_all_toppings








      



