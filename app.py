from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from datetime import datetime
from api.devices.devices import devices
from api.serviceLocations.serviceLocation import serviceLocation
from api.user.customer import customer
from api.util.validator import validate_date_format, validate_integer_text_format
from api.views.view import view
from db import init_app, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root123@localhost/shems'
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

@app.route('/user/<cust_id>/energyConsumed', methods=['GET'])
def customerEnergyConsumed(cust_id):
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    if not validate_date_format(start_date) or not validate_date_format(end_date):
        return render_template("error.html", error = {'status': 'error', 'message': 'Date is not in correct format'})
    if not validate_integer_text_format(cust_id):
        return jsonify({'status': 'error', 'message': 'Cust id can only be an integer check the URL'})
    
    params = {'cust_id': cust_id, 'start_date': start_date, 'end_date': end_date}
    query = text('''SELECT
                        sl.cust_id AS cust_id,
                        DATE(e.timestamp) AS Date,
                        SUM(e.value) AS `Energy Consumed`
                    FROM
                        service_loc sl
                    NATURAL JOIN
                        device d
                    NATURAL JOIN
                        event e
                    WHERE
                        sl.cust_id = :cust_id
                        AND e.label = 'energy use'
                        AND DATE(e.timestamp) >= :start_date
                        AND DATE(e.timestamp) < :end_date
                    GROUP BY
                        sl.cust_id,
                        DATE(e.timestamp)
                    ORDER BY
                        DATE(e.timestamp)''')
    result = db.session.execute(query, params)

    date_labels, energy_consumed_data = [], []
    for r in result:
        date_labels.append(r[1].strftime("%Y-%m-%d"))
        energy_consumed_data.append(r[2])

    return render_template("energyConsumed.html", date_labels = date_labels, values = energy_consumed_data)

if __name__ == '__main__':
    app.run(debug=True)
