from flask import render_template, redirect, request, session, flash, url_for, Response
from models import User, Order, Topping, Address


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
    return render_template('new_order.html')

def pizza_create():
    pizza_id = Order.create_order(request.form)
    session['pizza_id'] = pizza_id
    return redirect(url_for('order'))

#order page
def order_page():
    pizza = Order.get_order()
    return render_template('order.html', pizza = pizza)




