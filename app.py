from sqlite3.dbapi2 import connect, paramstyle
from flask import Flask
from flask import request, jsonify
import sqlite3

from flask import json

app = Flask(__name__)
app.config["DEBUG"] = True


def conn_db():
    conn = sqlite3.connect("makan.db")
    return conn


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''


@app.route('/api/foods/all', methods=['GET'])
def api_all():
    db = conn_db()
    db.row_factory = dict_factory
    cursor = db.cursor()
    all_foods = cursor.execute('SELECT * FROM food;').fetchall()

    return jsonify(all_foods)


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


@app.route('/api/foods', methods=['GET'])
def api_filter():
    query_parameters = request.args

    id = query_parameters.get('id')
    daerah = query_parameters.get('daerah')
    nama = query_parameters.get('nama')

    query = "SELECT * FROM food WHERE"
    to_filter = []

    db = conn_db()
    db.row_factory = dict_factory
    cursor = db.cursor()

    if id:
        query += ' id=? AND'
        to_filter.append(id)
    if daerah:
        query += ' daerah=? AND'
        to_filter.append(daerah)
    if nama:
        query += ' nama=? AND'
        to_filter.append(nama)
    if not (id or daerah or nama):
        return jsonify(cursor.execute('SELECT * FROM food;').fetchall())

    query = query[:-4] + ';'

    results = cursor.execute(query, to_filter).fetchall()

    return jsonify(results)


@app.route('/api/foods', methods=['POST'])
def add_food():

    query = "INSERT INTO food (nama, asal_daerah, deskripsi, foto) VALUES (?, ?, ?, ?)"

    params = request.get_json()
    nama = params["nama"]
    asal_daerah = params["asal_daerah"]
    deskripsi = params["deskripsi"]
    foto = params["foto"]

    db = conn_db()
    db.row_factory = dict_factory
    cursor = db.cursor()

    cursor.execute(query, [nama, asal_daerah, deskripsi, foto])
    db.commit()

    return "Data Berhasil ditambahkan"


app.run(port=5005)
