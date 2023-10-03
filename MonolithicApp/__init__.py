from flask import Flask, request
from MonolithicApp.Warehouse.WarehouseManager import WarehouseManager
from MonolithicApp.Orders.OrdersManager import OrdersManager
from MonolithicApp.Customers.CustomersManager import CustomersManager
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


@app.route("/newOrder", methods=["POST"])
def newOrder():
    if request.method == "POST":
        print("Ordine inviato:\n", request.data.decode())
        try:
            if request.is_json:
                OrdersManager().newOrder(request.get_json())
            else:
                return "No json provided"
        except DatabaseError as e:
            print(e.args[0])
            return "Database error."


@app.route("/registerCustomer", methods=["POST"])
def registerCustomer():
    if request.method == "POST":
        print("Registrazione nuovo cliente >\n", request.data.decode())
        try:
            if request.is_json:
                CustomersManager().addNewCustomer(request.get_json())
                return "Customer added"
            else:
                return "No json provided"
        except DatabaseError as e:
            print(e.args[0])
            return "Database error"

@app.route("/login", methods=["POST"])
def customerLogin():
    pass


if __name__ == "__main__":
    app.run(debug=True)