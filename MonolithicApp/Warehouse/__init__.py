from flask import Flask, request
from WarehouseManager import WarehouseManager
from psycopg2 import DatabaseError
from flask_restful import Api, Resource

app = Flask(__name__)


@app.route("/productsList", methods=["GET", "POST"])
def productList():
    if request.method == "GET":
        try:
            return WarehouseManager().getProductsList()
            # return "Ci sei riuscito!"
        except DatabaseError as e:
            print(e.args[0])
            return "Database error."
    elif request.method == "POST":
        print("Richiesta > ", request.data.decode())
        try:
            if request.is_json:
                # print(request.get_json())
                # print("Tipo > ", type(request.get_json()))
                # print("Headers > ", request.headers)
                WarehouseManager().addProduct(request.get_json())
                return "Inserito"
            else:
                return "Error - can't find Json file"
        except DatabaseError as e:
            print(e.args[0])
            return "Database error."


if __name__ == "__main__":
    app.run(debug=True)