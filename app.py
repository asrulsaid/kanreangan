# import library
from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS

# Inisiasi object flask
app = Flask(__name__)

# Inisiasi object flask_restful
api = Api(app)

# Inisiasi object flask_cors
CORS(app)

# Inisiasi variabel kosong bertipe Dictionary
identitas = {}

# Membuat class Resource


class ContohResource(Resource):
    # Method GET dan POST
    def get(self):
        # response = {"msg": "Haahahaahah"}

        return identitas

    def post(self):
        nama = request.form["nama"]
        umur = request.form["umur"]
        identitas["nama"] = nama
        identitas["umur"] = umur
        response = {"msg": "data berhasil dimasukan"}
        return response


# Setup Resource
api.add_resource(ContohResource, "/api", methods=["GET", "POST"])

if __name__ == "__main__":
    app.run(debug=True, port=5005)
