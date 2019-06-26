from flask import render_template, redirect, request, session, flash, url_for, Response
from models import User, Order, Topping, Address, Pizza, Topping_Menu, Size, Crust, Method


#Register page 
def root():
    if 'user_id' not in session:
        return redirect(url_for('users:new'))
    return redirect(url_for('dashboard'))

def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('users:new'))

    current_user = User.query.get(session['user_id'])
    
    return render_template('dashboard.html', 
                            user = current_user)

def new():
    return render_template('index.html')

def register_page():
    return render_template('register.html')

def login_page():
    return render_template('login.html')

def register():
    errors = User.register_validation(request.form)
    if errors:
        for error in errors:
            flash(error)
        return redirect(url_for('users:register_page'))
    user_id = User.user_create(request.form)
    session['user_id'] = user_id
    return redirect(url_for('dashboard'))

def login():
    valid, response = User.login_validation(request.form)
    if not valid:
        flash(response)
        return redirect(url_for('users:login_page'))
    session['user_id'] = response
    return redirect(url_for('dashboard'))

def logout():
    session.clear()
    return redirect(url_for('users:new'))

def account():
    current_user = User.query.get(session['user_id'])
    user_address = current_user.addresses[0]
    print(user_address)
    return render_template('user_account.html', user = current_user, address = user_address)

def user_update():
    user_id = session['user_id']
    update_user = User.edit_user(user_id, request.form)
    user = User.query.get(user_id)
    print('user_update')
    return redirect(url_for('dashboard'))

#pizza controllers
def pizza_dashboard():
    size = Size.get_all_size()
    method = Method.get_all_methods()
    crust = Crust.get_all_crust()
    topping_menu = Topping_Menu.get_all_toppings()
    return render_template('new_order.html', size = size, method = method, crust = crust, topping_menu = topping_menu)

def pizza_create():
    pizza = Order.new_order(request.form)
    session['pizza_id'] = pizza
    return redirect(url_for('order'))

#order page
def order_page():
    pizza = Pizza.get_user_order()
    return render_template('order.html', pizza = pizza)


#create apge
def create_page():
    size = Size.get_all_size()
    method = Method.get_all_methods()
    crust = Crust.get_all_crust()
    topping_menu = Topping_Menu.get_all_toppings()
    return render_template('staff.html', size = size, method = method, crust = crust, topping_menu = topping_menu)

def create_topping():
    topping_id = Topping_Menu.new(request.form)
    session['topping_id'] = topping_id
    return redirect(url_for('create_page'))

def create_size():
    size_id = Size.create_size(request.form)
    session['size_id'] = size_id
    return redirect(url_for('create_page'))

def create_crust():
    crust_id = Crust.create_crust(request.form)
    session['crust_id'] = crust_id
    return redirect(url_for('create_page'))

def create_method():
    method_id = Method.create_method(request.form)
    session['method_id'] = method_id
    return redirect(url_for('create_page'))


