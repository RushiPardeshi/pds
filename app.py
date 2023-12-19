from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from datetime import datetime
from api.devices.devices import devices
from api.serviceLocations.serviceLocation import serviceLocation
from api.user.customer import customer
from api.views.view import view
from db import init_app, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://rushipardeshi:animefreak@localhost/project'
app.register_blueprint(devices)
app.register_blueprint(serviceLocation)
app.register_blueprint(customer)
app.register_blueprint(view)
init_app(app)

# Sample data (you might want to use a database in practice)
service_locations = [
    {"loc_id": "101", "addr": "123 Main St", "zipcode": 12345},
    # Add more service location data
]

smart_devices = {
    "refrigerator": ["Bosch 800", "Samsung XYZ"],
    "AC": ["GE 4500", "Carrier 2000"],
    # Add more devices for each type
}

cust = [
    {"cust_id":"", "name": "", "cust_addr": ""}
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_location', methods=['POST'])
def add_location():
    # Get data from the form
    loc_id = request.form['loc_id']
    addr = request.form['addr']
    zipcode = request.form['zipcode']
    # Add new location to the list
    service_locations.append({"loc_id": loc_id, "addr": addr, "zipcode": zipcode})
    return render_template('index.html', locations=service_locations)

@app.route('/remove_location/<loc_id>')
def remove_location(loc_id):
    # Remove the location with the given loc_id
    for loc in service_locations:
        if loc['loc_id'] == loc_id:
            service_locations.remove(loc)
            break
    return render_template('index.html', locations=service_locations, devices=smart_devices)

@app.route('/add_device', methods=['POST'])
def add_device():
    # Get data from the form
    device_type = request.form['device_type']
    selected_model = request.form['selected_model']

    # Add new device to the list
    smart_devices[device_type].append(selected_model)
    return render_template('index.html', locations=service_locations, devices=smart_devices)

@app.route('/add_location', methods=['POST'])
def add_customer():
    cust_name = request.form['cust_name']
    cust_addr = request.form['cust_addr']

    cust.append()

@app.route('/login', methods=['GET','POST'])
def login():
    name = request.form.get("name")
    addr = request.form.get("address")
    result = db.session.execute(text(f"select * from customer where customer.name={name} and customer.bill_addr={addr}"))
    ans = result.fetchall()
    
    if len(ans) > 1:
      cust_id = ans[0][0]
      cust_name = ans[0][1]
    print(ans)

    return render_template("model.html")

@app.route('/{cust[cust_id]}/model', methods = ['GET','POST'])
def model():
    return render_template("register.html")

if __name__ == '__main__':
    app.run(debug=True)
