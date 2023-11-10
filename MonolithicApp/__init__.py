from flask import Flask, request, jsonify
from MonolithicApp.Warehouse.WarehouseManager import WarehouseManager
from MonolithicApp.Orders.OrdersManager import OrdersManager
from MonolithicApp.Customers.CustomersManager import CustomersManager
from MonolithicApp.Payments.PaymentsManager import PaymentsManager
from MonolithicApp.Authentication.AuthenticationManager import AuthenticationManager
from MonolithicApp.Authentication.AuthenticationManager import checkToken
from MonolithicApp.Shippings.ShippingManager import ShippingsManager
from MonolithicApp.Globals.Enumeratives import Roles
from psycopg2 import DatabaseError
import json
from flask_restful import Api, Resource

app = Flask(__name__)


@app.route("/productsList", methods=["GET", "POST"])
def productList():
    """
    Gestisce metodi GET e POST.
    - GET: restituisce l'elenco di tutti i prodotti presenti in magazzino con relative quantità
    - POST: permette ai fornitori di aggiungere prodotti nel magazzino
    """
    token = request.headers.get('Authorization')
    print("Token = ", token)
    validToken = _isValid_token(token)
    if not validToken[0]:
        return 401, json.dumps(validToken[1])
    token = validToken[2]

    # richiesta della lista di prodotti
    if request.method == "GET":
        if token['role'] != Roles.CUSTOMER.name:
            return json.dumps({"comment": "Unauthorized user"}), 401

        try:
            listOfProducts = WarehouseManager().getProductsList()
            print("Return ", len(listOfProducts), " products")
            return json.dumps(listOfProducts), 200
        except DatabaseError as e:
            print(e.args[0])
            return json.dumps({"comment": "Database error"}), 500

    elif request.method == "POST":  # inserimento prodotti
        print("Richiesta > ", request.data.decode())
        # verifica il ruolo del client, solo i fornitori possono inserire prodotti
        if token['role'] != Roles.SUPPLIER.name:
            return json.dumps({"comment": "Insufficient privileges"}), 401

        try:
            if request.is_json:
                WarehouseManager().addProduct(request.get_json())
                return json.dumps({"comment": "Product(s) inserted"}), 200
            else:
                return json.dumps({"comment": "Error - can't find json file"}), 400
        except DatabaseError as e:
            print(e.args[0])
            return json.dumps({"comment": "Database error"}), 500

    else:
        return 405, json.dumps({"comment": f"Method {request.method} not supported"})


@app.route("/newOrder", methods=["POST"])
def newOrder():
    """
    Gestisce la creazione di un nuovo ordine
    """
    token = request.headers.get('Authorizarion')
    print("Token > ", token)
    validToken = _isValid_token(token)
    if validToken[0]:
        token = validToken[2]
        print(validToken[1])
    else:
        return 401, json.dumps(validToken[1])


    if request.method == "POST":
        if token['role'] != Roles.CUSTOMER.name:
            return 401, json.dumps({"comment": "This user can't make new orders"})

        print("Ordine inviato:\n", request.data.decode())
        try:
            if request.is_json:
                response = OrdersManager().newOrder(request.get_json())
                return 201, json.dumps(response)
            else:
                return 400, json.dumps({"comment": "No json provided"})
        except DatabaseError as e:
            print(e.args[0])
            return 500, json.dumps({"comment": "Database error"})

    else:
        return 405, json.dumps({"comment": f"Method {request.method} not supported"})


@app.route("/registerCustomer", methods=["POST"])
def registerCustomer():
    """
    Permette la registrazione di un nuovo cliente
    """
    if request.method == "POST":
        print("Registrazione nuovo cliente >\n", request.data.decode())
        try:
            if request.is_json:
                CustomersManager().addNewCustomer(request.get_json())
                return 201, json.dumps({"comment": "Customer added"})
            else:
                return 400, json.dumps({"comment": "No json provided"})
        except DatabaseError as e:
            print(e.args[0])
            return 500, json.dumps({"comment": "Database error"})
    else:
        return 405, json.dumps({"comment": f"Method {request.method} not supported"})


@app.route("/login", methods=["POST"])
def customerLogin():
    if request.method == "POST":
        print("Sent request:\n", request.data.decode())
        if request.is_json:
            response = AuthenticationManager().authenticateUser(request.get_json())
            return json.dumps(response), 200
        else:
            return json.dumps({"comment": "Credentials not provided"}), 400
    else:
        return json.dumps({"comment": f"Method {request.method} not supported"}), 500


@app.route("/payOrder", methods=["POST"])
def payOrder():
    token = json.loads(request.headers.get('Authorizarion'))
    validToken = _isValid_token(token)
    if not validToken[0]:
        return 401, json.dumps(validToken[1])

    if request.method == "POST":
        print("Incoming order summary:\n", request.data.decode())
        if request.is_json:
            response = PaymentsManager().pay(request.get_json())
            return 200, json.dumps(response)
        else:
            return 400, json.dumps({"comment": "No json provided"})
    else:
        return 405, json.dumps({"comment": f"Method {request.method} not supported"})


@app.route("/trackOrder", methods=["GET"])
def trackOrder():
    if request.method == "GET":
        trackingID = int(request.args.get('id'))
        print("Tracking ID = ", trackingID)
        return 200, json.dumps(ShippingsManager().trackOrder(trackingID))


def _isValid_token(token):
    """
    Controlla se il token fornito è ancora valido
    :param token: il token in formato stringa
    :return: Booleano, un commento sotto forma di dizionario, il token decodificato oppure None
    """
    # token = json.loads(token)
    checked = checkToken(token)
    if checked[0]:
        return True, {"comment": "Token is valid"}, checked[1]
    return False, {"comment": "Invalid token"}, None



if __name__ == "__main__":
    app.run(debug=True)