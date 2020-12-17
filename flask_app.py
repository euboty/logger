import datetime
import sqlite3

from flask import Flask, jsonify, request, abort
from loguru import logger


from queries import (
    get_last_temp, get_sauna_dates, get_sauna_week_data, get_sauna_day_data,
    get_last_vibration, get_pool_dates, get_pool_week_data, get_pool_day_data,
)

from monitor import read_temperature
from vibration import read_vibration

db_name = '/home/pi/logger/templog.db'


app = Flask(__name__)


@app.route("/api/doehlen-info")
def doehlen_info():
    # open db and set cursor return to Row (dict like)
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row
    curs = conn.cursor()

    last_temp = get_last_temp(curs)
    last_vibration = get_last_vibration(curs)
    sauna_dates = get_sauna_dates(curs)
    pool_dates = get_pool_dates(curs)
    server_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    conn.close()

    return {
        'server_time': server_time,
        'last_temperature': last_temp,
        'last_vibration': last_vibration,
        'sauna_dates': sauna_dates,
        'pool_dates': pool_dates,
    }


@app.route("/api/sauna/week")
def sauna_chart():
    # open db and set cursor return to Row (dict like)
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row
    curs = conn.cursor()
    data = get_sauna_week_data(curs)
    conn.close()

    return jsonify(data)


@app.route("/api/pool/week")
def pool_chart():
    # open db and set cursor return to Row (dict like)
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row
    curs = conn.cursor()
    data = get_pool_week_data(curs)
    conn.close()

    return jsonify(data)


@app.route("/api/sauna/day")
def sauna_day():
    # open db and set cursor return to Row (dict like)
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row
    curs = conn.cursor()

    day = request.args.get('day')
    data = get_sauna_day_data(curs, day)
    conn.close()

    return jsonify(data)


@app.route("/api/pool/day")
def pool_day():
    # open db and set cursor return to Row (dict like)
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row
    curs = conn.cursor()

    day = request.args.get('day')
    data = get_pool_day_data(curs, day)
    conn.close()

    return jsonify(data)

# @app.route("/api/pool/minutes")
# def pool_minutes():
#     # open db and set cursor return to Row (dict like)
#     conn = sqlite3.connect(db_name)
#     conn.row_factory = sqlite3.Row
#     curs = conn.cursor()

#     day = request.args.get('day')
#     return jsonify(get_pool_day_minutes(curs, day))


@app.route("/api/sauna/now")
def measure_temperature():
    # run the measure code and return temperature
    try:
        return jsonify(read_temperature())
    except Exception:
        logger.exception("Could not read temperature")
        return "Could not read temperature", 500


@app.route("/api/pool/now")
def measure_vibration():
    # run the measure code and return temperature
    try:
        return jsonify(read_vibration())
    except Exception:
        logger.exception("Could not read vibration")
        return "Could not read vibration", 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
