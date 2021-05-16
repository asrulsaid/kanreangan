# import library
from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS
import json

# Inisiasi object flask
app = Flask(__name__)

# Inisiasi object flask_restful
api = Api(app)

# Inisiasi object flask_cors
CORS(app)

# Inisiasi variabel kosong bertipe Dictionary
newData = {}
newData['people'] = []


def write_json(new_data, filename='data.json'):
    with open(filename, 'r+') as file:
        file_data = json.load(file)
        file_data.update(new_data)
        file.seek(0)
        json.dump(file_data, file)

# Membuat class Resource


class ContohResource(Resource):
    # Method GET dan POST

    def get(self, nama):
        # response = {"msg": "Haahahaahah"}
        with open('data.json') as json_file:
            data = json.load(json_file)
            for i in range(int(len(data['people']))):
                msg = ''
                if data['people'][i]['nama'] == nama:
                    msg = 'ada'
                    break
                else:
                    msg = 'tidak'
            return msg

    def post(self):
        nama = request.form["nama"]
        umur = request.form["umur"]
        newData['people'].append({"nama": nama, "umur": umur})
        write_json(newData)
        response = {"msg": "data berhasil dimasukan"}
        return response


# Setup Resource
api.add_resource(ContohResource, "/api/<string:nama>")
# api.add_resource(ContohResource, "/search/<string:nama>")

if __name__ == "__main__":
    app.run(debug=True, port=5005)
