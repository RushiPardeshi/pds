from flask import Flask, render_template, request, jsonify, Blueprint
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from datetime import datetime
from db import db
from ..util.validator import validate_input_address_format, validate_integer_text_format, validate_zipcode

serviceLocation = Blueprint('serviceLocation', __name__)

# get all service locations
@serviceLocation.route("/locations", methods=['GET'])
def getLocations():
    result = db.session.execute(text("Select * from service_loc")).fetchall()
    # dic = {
    #     'loc_id': None,
    #     'cust_id': None,
    #     'Address': None,
    #     'Registered date': None,
    #     'area': None,
    #     'nbed': None,
    #     'noccupant': None,
    #     'zipcode': None
    # }
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
    print(results)
    return jsonify({'result': results})

# get service location by id
@serviceLocation.route("/locations/<loc_id>", methods=['GET'])
def getLocationsByUserID(loc_id):
    result = db.session.execute(text('''Select * 
                                     from service_loc sl  
                                     where sl.loc_id = :loc_id'''), params={'loc_id': loc_id}).fetchall()
    return result

# add location
@serviceLocation.route("/location", methods=['POST'])
def addLocation():
    try:
        payload = request.get_json()
        loc_id = getNextLocId()
        cust_id = payload['cust_id']
        if not validate_integer_text_format(cust_id):
            return render_template("error.html", error = {'status': 'validation error', 'msg': "validation error occured in customer id pls check"})
        addr = payload['addr']
        if not validate_input_address_format(addr):
            return render_template("error.html", error = {'status': 'validation error', 'msg': 'validation error occured, pls verify address field'})
        date = datetime.today()
        area = payload['area']
        num_beds = payload['nbed']
        num_occupants = payload['noccupants']
        if not validate_integer_text_format(area) or not validate_integer_text_format(num_beds) or not validate_integer_text_format(num_occupants):
            return render_template("error.html", error = {'status': 'validation error', 'msg': "validation error occured, pls check fields"})
        zipcode = payload['zipcode']
        if not validate_zipcode(zipcode):
            return render_template("error.html", error = {'status': 'validation error', 'msg': "validation error occured in zipcode"})
        params = {
            'loc_id': loc_id,
            'cust_id': cust_id,
            'addr': addr,
            'date': date,
            'area': area,
            'nbed': num_beds,
            'noccupants': num_occupants,
            'zipcode': zipcode
        }
        db.session.execute(text('''Insert into service_loc(loc_id, cust_id, addr, date, area, num_beds, num_occupants, zipcode) 
                                values (:loc_id, :cust_id, :addr, :date, :area, :nbed, :noccupants, :zipcode)'''), params)
        db.session.commit()
        return jsonify({'status': 'error', 'msg': 'Record added successfully'})
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

# delete device
@serviceLocation.route("/location/<loc_id>", methods=['DELETE'])
def deleteLocation(loc_id):
    try:
        db.session.execute(text("Delete from service_loc where loc_id=:loc_id"), params={'loc_id': loc_id})
        db.session.commit()
        return jsonify({'status': 'success', 'msg': 'Record deleted successfully'})
    except Exception as e:
        return render_template("error.html", error = {'status': 'error', 'message': str(e)})
    
def getNextLocId():
    # write a sequence in the database and get id from it
    last_db_id = db.session.execute(text("Select loc_id from service_loc order by loc_id desc")).fetchone()[0]
    return str(int(last_db_id)+1)