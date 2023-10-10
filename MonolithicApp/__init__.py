from flask import Flask, request
from MonolithicApp.Warehouse.WarehouseManager import WarehouseManager
from MonolithicApp.Orders.OrdersManager import OrdersManager
from MonolithicApp.Customers.CustomersManager import CustomersManager
from MonolithicApp.Payments.PaymentsManager import PaymentsManager
from MonolithicApp.Authentication.AuthenticationManager import AuthenticationManager
from MonolithicApp.Shippings.ShippingManager import ShippingsManager
from psycopg2 import DatabaseError
import json
from flask_restful import Api, Resource

app = Flask(__name__)


@app.route("/productsList", methods=["GET", "POST"])
def productList():
    if request.method == "GET":
        try:
            return WarehouseManager().getProductsList()
        except DatabaseError as e:
            print(e.args[0])
            return json.dumps({"comment": "Database error"})
    elif request.method == "POST":
        print("Richiesta > ", request.data.decode())
        try:
            if request.is_json:
                WarehouseManager().addProduct(request.get_json())
                return json.dumps({"comment": "Product inserted"})
            else:
                return json.dumps({"comment": "Error - can't find json file"})
        except DatabaseError as e:
            print(e.args[0])
            return json.dumps({"comment": "Database error"})
    else:
        return json.dumps({"comment": f"Method {request.method} not supported"})


@app.route("/newOrder", methods=["POST"])
def newOrder():
    if request.method == "POST":
        print("Ordine inviato:\n", request.data.decode())
        try:
            if request.is_json:
                response = OrdersManager().newOrder(request.get_json())
                return json.dumps(response)
            else:
                return json.dumps({"comment": "No json provided"})
        except DatabaseError as e:
            print(e.args[0])
            return json.dumps({"comment": "Database error"})
    else:
        return json.dumps({"comment": f"Method {request.method} not supported"})


@app.route("/registerCustomer", methods=["POST"])
def registerCustomer():
    if request.method == "POST":
        print("Registrazione nuovo cliente >\n", request.data.decode())
        try:
            if request.is_json:
                CustomersManager().addNewCustomer(request.get_json())
                return json.dumps({"comment": "Customer added"})
            else:
                return json.dumps({"comment": "No json provided"})
        except DatabaseError as e:
            print(e.args[0])
            return json.dumps({"comment": "Database error"})
    else:
        json.dumps({"comment": f"Method {request.method} not supported"})


@app.route("/login", methods=["POST"])
def customerLogin():
    if request.method == "POST":
        print("Sent request:\n", request.data.decode())
        if request.is_json:
            response = AuthenticationManager().authenticateUser(request.get_json())
            return json.dumps(response)
        else:
            return json.dumps({"comment": "No json provided"})
    else:
        return json.dumps({"comment": "No json provided"})


@app.route("/payOrder", methods=["POST"])
def payOrder():
    if request.method == "POST":
        print("Incoming order summary:\n", request.data.decode())
        if request.is_json:
            response = PaymentsManager().pay(request.get_json())
            return json.dumps(response)
        else:
            return json.dumps({"comment": "No json provided"})
    else:
        json.dumps({"comment": f"Method {request.method} not supported"})


@app.route("/trackOrder", methods=["GET"])
def trackOrder():
    if request.method == "GET":
        trackingID = int(request.args.get('id'))
        print("Tracking ID = ", trackingID)
        return json.dumps(ShippingsManager().trackOrder(trackingID))


if __name__ == "__main__":
    app.run(debug=True)