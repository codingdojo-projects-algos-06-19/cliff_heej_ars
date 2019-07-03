from flask import render_template, redirect, request, session, flash, url_for, Response
import stripe
from models import User, Order, Topping, Address, Random_order

pub_key = 'pk_test_LnWQOJnxHrgUjxeLPUQHOFf100IknAvSln'
secret_key = 'sk_test_pcRm5ZoW1TZHWdWGW8dAAqqZ00lNAjivvG'


stripe.api_key = secret_key

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
    session['email'] = request.form['email']
    return redirect(url_for('dashboard'))

def logout():
    session.clear()
    return redirect(url_for('users:new'))

def account():
    if 'user_id' not in session:
        return redirect(url_for('users:new'))
    current_user = User.query.get(session['user_id'])
    user_address = current_user.addresses[0]
    print(user_address)
    return render_template('user_account.html', user = current_user, address = user_address)

def user_update():
    if 'user_id' not in session:
        return redirect(url_for('users:new'))
    user_id = session['user_id']
    update_user = User.edit_user(user_id, request.form)
    user = User.query.get(user_id)
    print('user_update')
    return redirect(url_for('dashboard'))

def pizza_update():
    order_id = session['order_id']
    update_order = Order.edit_order(order_id, request.form)
    order = Order.query.get(order_id)
    print('order')
    return redirect(url_for('order'))

#pizza controllers
def pizza_dashboard():
    if 'user_id' not in session:
        return redirect(url_for('users:new'))
    # size = Size.get_all_size()
    # method = Method.get_all_methods()
    # crust = Crust.get_all_crust()
    # topping_menu = Topping_Menu.get_all_toppings()
    topping = Topping.get_all()
    current_user = User.query.get(session['user_id'])

    return render_template('new_order.html', topping = topping, user = current_user)

def pizza_create():
    if 'user_id' not in session:
        return redirect(url_for('users:new'))
    user_id = session['user_id']
    order_id = Order.create_order(user_id, request.form)
    session['order_id'] = order_id
    return redirect(url_for('order'))

#order page
def order_page():
    if 'user_id' not in session:
        return redirect(url_for('users:login_page'))
    # current_order = Order.query.get(session['user_id'])
    # user_order = Topping.query.get(session['topping_id'])
    pizza = Order.get_order()
    topping = Topping.get_order_topping(session['order_id'])
    total = Order.total
    current_user = User.query.get(session['user_id'])
    return render_template('order.html', pizza = pizza, topping = topping, total = total, user = current_user)

def order_delete(id):
    print(request.form)
    delete = Order.delete(id)
    return redirect(url_for('order'))

def add(topping_id):
    Topping.add(session['user_id'], topping_id)
    return redirect(url_for('order'))

def topping_delete(id):
    Topping.delete(id)
    return redirect(url_for('order'))

#create apge
def create_page():
    random_pizza = Random_order.all_random_pizza()
    return render_template('staff.html', random = random_pizza)

def create_random_pizza():
    random_order_id = Random_order.new_pizza(request.form)
    # topping_id = Topping_Menu.new(request.form)
    session['random_order_id'] = random_order_id
    return redirect(url_for('create_page'))

def order_success():
    current_user = User.query.get(session['user_id'])
    return render_template('success.html', user = current_user)

def charge_order():
    print(request.form)
    # user = stripe.Customer.create(email=session['user_id'], source = request.form['stripeToken'])
    # charge = stripe.Charge.create(
    #     user = user.id,
    #     total = int(float(request.form['total'])*100),
    #     currency = 'usd',
    #     source = request.form
    # )
    return redirect(url_for('success'))
# def create_size():
#     size_id = Size.create_size(request.form)
#     session['size_id'] = size_id
#     return redirect(url_for('create_page'))

# def create_crust():
#     crust_id = Crust.create_crust(request.form)
#     session['crust_id'] = crust_id
#     return redirect(url_for('create_page'))

# def create_method():
#     method_id = Method.create_method(request.form)
#     session['method_id'] = method_id
#     return redirect(url_for('create_page'))

