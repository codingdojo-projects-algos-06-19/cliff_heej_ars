from flask import render_template, redirect, request, session, flash, url_for, Response
from models import User, Pizza


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
    return render_template('user_account.html', user = current_user)

def user_update():
    User.edit_user(request.form)
    print('user_update')
    return redirect(url_for('users:update'))

#pizza controllers
def pizza_dashboard():
    return render_template('new_order.html')

def pizza_create():
    pizza_id = Pizza.create_pizza(request.form)
    session['pizza_id'] = pizza_id
    return redirect('pizza:create')

#order page
def order_page():
    pizza = Pizza.get_pizza()
    return render_template('order.html', pizza = pizza)




