from flask import Blueprint, Flask, redirect, render_template, request, jsonify, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import true
from sqlalchemy.sql import text
from datetime import datetime
from api.util.validator import validate_input_address_format, validate_input_text_format, validate_integer_text_format
from db import db

customer = Blueprint('customer', __name__)

cust = []

# get customer with user id
@customer.route("/user_login", methods=['GET'])
def getCustomerByUserID():
    name = request.args.get('name')
    address = request.args.get('address')
    if not validate_input_address_format(address):
        return render_template("error.html", error = {'status': 'validation error', 'message': 'address not in correct format'})
    if not validate_input_text_format(name):
        return render_template("error.html", error = {'status': 'validation error', 'message': 'name not in correct format'})
    # name = request.form['name']
    # address = request.form['address']
    result = db.session.execute(text('''Select * 
                                     from customer c  
                                     where c.name = :name and c.bill_addr = :address'''), params={'name': name, 'address': address}).fetchone()
    
    # dic = {'name': result[1], 'address': result[2]}
    cust_id = result[0] if result else render_template("error.html", error = {'status': 'unexpected error', 'message': 'Unexpected error'})
    curr_cust = {"cust_id": cust_id, "name":name, "bill_addr": address}
    if curr_cust not in cust:
        cust.append(curr_cust)
    return render_template('customer.html', name=name,cust_id=cust_id)


# get all locations for a customer
@customer.route("/user/<cust_id>/locations", methods=['GET'])
def getLocationsByUserID(cust_id):
    if not validate_integer_text_format(cust_id):
        return render_template("error.html", error = {'status': 'validation error', 'message': 'cust id not in correct format'})
    result = db.session.execute(text('''Select * from service_loc where cust_id = :id and enabled=1'''), params={'id': cust_id}).fetchall()
    results = []
    for r in result:
        dic = {}
        dic['loc_id'] = r[0]
        dic['cust_id'] = r[1]
        dic['Address'] = r[2]
        dic['Registered date'] = str(r[3])
        dic['area'] = r[4]
        dic['nbed'] = r[5]
        dic['noccupant'] = r[6]
        dic['zipcode'] = r[7]
        results.append(dic)
    return results

@customer.route("/user/<cust_id>/locations/<loc_id>/devices", methods=['GET'])
def getDevicesByLoc(cust_id, loc_id):
    if not validate_integer_text_format(cust_id) or not validate_integer_text_format(loc_id):
        return render_template("error.html", error = {'status': 'validation error', 'message': 'some id not in correct format'})
    result = db.session.execute(text('''Select d.dev_id, m.model_name, m.model_type 
                                     from device d 
                                     natural join service_loc sl 
                                     natural join model m
                                     where sl.cust_id = :id and sl.loc_id = :loc_id and d.enabled=1'''), params={'id': cust_id, 'loc_id': loc_id}).fetchall()
    results = []
    for r in result:
        dic = {}  
        dic['dev_id'] = r[0]
        dic['model_name'] = r[1]
        dic['model_type'] = r[2]
        results.append(dic)
    
    return results
    

# add user
@customer.route("/user_register", methods=['POST'])
def addUser():
    try:
        # print('working')
        payload = request.get_json()
        cust_id = getNextCustId()
        addr = payload['address']
        name = payload['name']
        if not validate_input_address_format(addr):
            return jsonify({'status': 'validation error', 'message': 'address not in correct format'})
        if not validate_input_text_format(name):
            return jsonify({'status': 'validation error', 'message': 'name not in correct format'})
        params = {'addr': addr, 'name': name, 'cust_id': cust_id}
        db.session.execute(text('''Insert into customer(cust_id, name, bill_addr) values 
                                (:cust_id, :name, :addr)'''), params)
        db.session.commit()
        # print(url_for('login'))
        # return jsonify({'status': 'success', 'msg': 'User created successfully, go back and login'})
        return redirect(url_for('login'))
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

# delete user
@customer.route("/user/<cust_id>/del", methods=['DELETE'])
def deleteDevice(cust_id):
    if not validate_integer_text_format(cust_id):
        return render_template("error.html", error = {'status': 'validation error', 'message': 'cust id not in correct format'})
    try:
        db.session.execute(text("Delete from customer where cust_id=:id"), params={'id': cust_id})
        db.session.commit()
        # return jsonify({'status': 'error', 'msg': 'Record deleted successfully'})
        return render_template("login.html")
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})
    
def getNextCustId():
    # write a sequence in the database and get id from it
    last_db_id = db.session.execute(text("Select cust_id from customer where cust_id REGEXP '^[0-9]+$' order by cust_id desc")).fetchone()
    last_db_id = last_db_id[0] if last_db_id else render_template("error.html", error = {'status': 'unexpected error', 'message': 'Unexpected error'})
    return str(int(last_db_id)+1)