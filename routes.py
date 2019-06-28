from config import app
import controllers

#Master routes
#@app.route('/') #this part goes to route
#def root():
# return render_template(
#        'index.html',
#       )
app.add_url_rule('/', view_func=controllers.root, endpoint='root')
app.add_url_rule('/dashboard', view_func=controllers.dashboard, endpoint='dashboard')

#Register
app.add_url_rule('/users/new', view_func=controllers.new, endpoint='users:new')
app.add_url_rule('/users/register_page', view_func=controllers.register_page, endpoint='users:register_page')
app.add_url_rule('/users/register', view_func=controllers.register, endpoint='users:register', methods=['POST'])
app.add_url_rule('/users/login_page', view_func=controllers.login_page, endpoint='users:login_page')
app.add_url_rule('/users/login', view_func=controllers.login, endpoint='users:login', methods=['POST'])
app.add_url_rule('/users/account', view_func=controllers.account, endpoint='users:account')
app.add_url_rule('/logout', view_func=controllers.logout, endpoint='users:logout')
app.add_url_rule('/users/update', view_func=controllers.user_update, endpoint='users:update', methods=['POST'])

#Pizza
app.add_url_rule('/pizza/dashboard', view_func=controllers.pizza_dashboard, endpoint='pizza:dashboard')
app.add_url_rule('/pizza/create', view_func=controllers.pizza_create, endpoint='pizza:create', methods=['POST'])

#Oder
app.add_url_rule('/order', view_func=controllers.order_page, endpoint='order')

# #create size, method, crust, toppings
# app.add_url_rule('/create_page', view_func=controllers.create_page, endpoint='create_page')
# app.add_url_rule('/create_topping', view_func=controllers.create_topping, endpoint='create:topping', methods=['POST'])
# app.add_url_rule('/create_size', view_func=controllers.create_size, endpoint='create:size', methods=['POST'])
# app.add_url_rule('/create_crust', view_func=controllers.create_crust, endpoint='create:crust', methods=['POST'])
# app.add_url_rule('/create_method', view_func=controllers.create_method, endpoint='create:method', methods=['POST'])