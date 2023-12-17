from flask import Flask, render_template, request, jsonify, Blueprint
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from datetime import datetime
from db import db

view = Blueprint('view', __name__)

#daily energy consumption for selected time period
@view.route('/user/<cust_id>/energyConsumed', methods=['GET'])
def customerEnergyConsumed(cust_id):
    start_date = request.get_json()['start_date']
    end_date = request.get_json()['end_date']
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
                        e.label = 'energy use'
                        AND DATE(e.timestamp) >= :start_date
                        AND DATE(e.timestamp) < :end_date
                    GROUP BY
                        sl.cust_id,
                        DATE(e.timestamp)''')
    result = db.session.execute(query, params)

    date_labels, energy_consumed_data = [], []
    for r in result:
        date_labels.append(r[1])
        energy_consumed_data(r[2])
    
    return render_template("energyConsumed.html", date_labels = date_labels, values = energy_consumed_data)


@view.route('/user/<cust_id>/energyCompare/<loc_id>', methods=['GET'])
def locationEnergyUsedAgainstOtherLocations(cust_id, loc_id):
    start_date = request.get_json()['start_date']
    end_date = request.get_json()['end_date']
    params = {'cust_id': cust_id, 'start_date': start_date, 'end_date': end_date}

    query = text('''SELECT
                        sl1.loc_id AS service_location_id,
                        sl1.addr AS address,
                        SUM(e1.value) AS energy_consumed,
                        (SUM(e1.value) / AVG(similar_sl.total_energy_consumption)) * 100 AS relative_energy_consumed_percentage
                    FROM
                        service_loc sl1
                    JOIN
                        device d1 ON d1.loc_id = sl1.loc_id
                    JOIN
                        event e1 ON d1.dev_id = e1.dev_id
                    JOIN
                        (
                            SELECT
                                sl2.loc_id AS loc_id,
                                AVG(e2.value) AS total_energy_consumption,
                                sl2.num_occupants AS num_occupants,
                                sl2.area AS area
                            FROM
                                service_loc sl2
                            JOIN
                                device d ON sl2.loc_id = d.loc_id
                            JOIN
                                event e2 ON e2.dev_id = d.dev_id
                            WHERE
                                DATE(e2.timestamp) >= :start_date
                                AND DATE(e2.timestamp) < :end_date
                            GROUP BY
                                sl2.loc_id
                        ) AS similar_sl 
                    ON sl1.area BETWEEN similar_sl.area * 0.95 AND similar_sl.area * 1.05 
                    AND sl1.num_occupants BETWEEN similar_sl.num_occupants - 2 AND similar_sl.num_occupants + 2
                    AND similar_sl.loc_id != sl1.loc_id
                    WHERE
                        sl1.cust_id = :cust_id
                        AND DATE(e1.timestamp) >= :start_date
                        AND DATE(e1.timestamp) < :end_date
                    GROUP BY
                        sl1.loc_id''')
    
    result = db.session.execute(query, params)

    address, energy_consumed, energy_consumption_percentage = [], [], []
    for r in result:
        address.append(r[1])
        energy_consumed.append(r[2])
        energy_consumption_percentage.append(r[3])

    return render_template('comparison.html', labels = address, energy_consumed = energy_consumed, relative_percentage_data = energy_consumption_percentage)