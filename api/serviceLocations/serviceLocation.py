from flask import Flask, render_template, request, jsonify, Blueprint
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from datetime import datetime
from db import db

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
def getLocationsByUserID():
    result = db.session.execute(text('''Select * 
                                     from service_loc sl  
                                     where sl.loc_id = ?'''), (loc_id, )).fetchall()
    return result

# add location
@serviceLocation.route("/location", methods=['POST'])
def addLocation():
    try:
        payload = request.get_json()
        loc_id = getNextLocId()
        cust_id = payload['cust_id']
        addr = payload['addr']
        date = datetime.today()
        area = payload['area']
        num_beds = payload['nbed']
        num_occupants = payload['noccupants']
        zipcode = payload['zipcode']
        device_id = str(getNextLocId())
        db.session.execute(text('''Insert into service_loc(loc_id, cust_id, addr, date, area, num_beds, num_occupants, zipcode) 
                                values (?,?,?,?,?,?,?,?)'''), (loc_id, cust_id, addr, date, area, num_beds, num_occupants, zipcode, ))
        db.session.commit()
        return jsonify({'status': 'error', 'msg': 'Record added successfully'})
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

# delete device
@serviceLocation.route("/location/<loc_id>", methods=['DELETE'])
def deleteLocation():
    try:
        db.session.execute(text("Delete from service_loc where dev_id=?"), (loc_id,))
        db.session.commit()
        return jsonify({'status': 'error', 'msg': 'Record deleted successfully'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})
    
def getNextLocId():
    # write a sequence in the database and get id from it
    last_db_id = db.session.execute(text("Select loc_id from service_loc order by loc_id desc")).fetchone()['loc_id']
    last_db_id_number = int(last_db_id.split("-")[1])
    return 'l-' + str(last_db_id_number+1)