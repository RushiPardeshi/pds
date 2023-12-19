from flask import Blueprint, Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from datetime import datetime
from db import db
from validator import validate_integer_text_format, validate_input_text_format, validate_input_address_format

customer = Blueprint('customer', __name__)

# get customer with user id
@customer.route("/user", methods=['GET'])
def getCustomer():
    name = request.form['name']
    address = request.form['address']
    result = db.session.execute(text('''Select * 
                                     from customer c  
                                     where c.name = :name and c.bill_address = :address'''), params={'name': name, 'address': address}).fetchone()
    # results = []
    dic = {'name': result[1], 'address': result[2]}
    # for r in result:
    #     dic = {}
    #     dic['name'] = r[1]
    #     dic['address'] = r[2]
    #     results.append(dic)
    return dic

# get all locations for a customer
@customer.route("/user/<cust_id>/locations", methods=['GET'])
def getLocationsByUserID(cust_id):
    if not validate_integer_text_format(cust_id):
        return jsonify({'status': 'error', 'message': 'Cust id can only be an integer check the URL'})
    result = db.session.execute(text('''Select * from service_loc where cust_id = :id'''), params={'id': cust_id}).fetchall()
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
    print(result)
    return results

# get devices list with user id
@customer.route("/user/<cust_id>/devices", methods=['GET'])
def getDevicesByUserID(cust_id):
    if not validate_integer_text_format(cust_id):
        return jsonify({'status': 'error', 'message': 'Cust id can only be an integer check the URL'})
    result = db.session.execute(text('''Select d.dev_id, m.model_name, m.model_type 
                                     from device d 
                                     natural join service_loc sl 
                                     natural join model m
                                     where sl.cust_id = :id'''), params={'id': cust_id}).fetchall()
    results = []
    for r in result:
        dic = {}
        dic['dev_id'] = r[0]
        dic['model_name'] = r[1]
        dic['model_type'] = r[2]
    return result

# add user
@customer.route("/user", methods=['POST'])
def addLocation():
    try:
        payload = request.get_json()
        cust_id = getNextCustId()
        addr = payload['addr']
        name = payload['name']
        if not validate_input_text_format(name) or not validate_input_address_format(addr):
            return jsonify({'status': 'error', 'message': 'Some fields entered do not match the required format of the field'})
        params = {'addr': addr, 'name': name, 'cust_id': cust_id}
        db.session.execute(text('''Insert into customer(cust_id, name, bill_addr) values 
                                (:cust_id, :name, :addr)'''), params)
        db.session.commit()
        return jsonify({'status': 'error', 'msg': 'Record added successfully'})
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

# delete user
@customer.route("/user/<cust_id>", methods=['DELETE'])
def deleteDevice(cust_id):
    if not validate_integer_text_format(cust_id):
        return jsonify({'status': 'error', 'message': 'Cust id can only be an integer check the URL'})
    try:
        db.session.execute(text("Delete from customer where cust_id=:id"), params={'id': cust_id})
        db.session.commit()
        return jsonify({'status': 'error', 'msg': 'Record deleted successfully'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})
    
def getNextCustId():
    # write a sequence in the database and get id from it
    last_db_id = db.session.execute(text("Select cust_id from customer order by cust_id desc")).fetchone()[0]
    return str(int(last_db_id)+1)