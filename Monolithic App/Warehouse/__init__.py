from flask import Flask, request
from WarehouseManager import WarehouseManager
from flask_restful import Api, Resource

app = Flask(__name__)


@app.route("/productsList", methods=["GET","POST"])
def productList():
    if request.method == "GET":
        return WarehouseManager().getProductsList()
    elif request.method == "POST":
        return "Received"


if __name__ == "__main__":
    app.run(debug=True)