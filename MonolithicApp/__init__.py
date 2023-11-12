from flask import Flask, request
from psycopg2 import DatabaseError
import json
import logging

from MonolithicApp.Warehouse.WarehouseManager import WarehouseManager
from MonolithicApp.Orders.OrdersManager import OrdersManager
from MonolithicApp.Customers.CustomersManager import CustomersManager
from MonolithicApp.Payments.PaymentsManager import PaymentsManager
from MonolithicApp.Authentication.AuthenticationManager import AuthenticationManager
from MonolithicApp.Authentication.AuthenticationManager import checkToken
from MonolithicApp.Shippings.ShippingManager import ShippingsManager
from MonolithicApp.Globals.Enumeratives import Roles

app = Flask(__name__)
loggingLevel = logging.CRITICAL  # livello di logging valido per tutto il progetto
logging.basicConfig(level=loggingLevel, format="%(asctime)s - %(levelname)s - %(message)s")


@app.route("/productsList", methods=["GET", "POST"])
def productList():
    """
    Gestisce metodi GET e POST.
    - GET: restituisce l'elenco di tutti i prodotti presenti in magazzino con relative quantità
    - POST: permette ai fornitori di aggiungere prodotti nel magazzino
    """
    logger = logging.getLogger("productsList_log")

    token = request.headers.get('Authorization')
    logger.info(f"Token = {token}")
    validToken = _isValid_token(token)
    if not validToken[0]:
        return json.dumps(validToken[1]), 401
    token = validToken[2]

    # richiesta della lista di prodotti
    if request.method == "GET":
        if token['role'] != Roles.CUSTOMER.name:
            return json.dumps({"comment": "Unauthorized user"}), 401

        try:
            listOfProducts = WarehouseManager().getProductsList()
            logger.debug(f"Return {len(listOfProducts)} products")
            return json.dumps(listOfProducts), 200
        except DatabaseError as e:
            print(e.args[0])
            return json.dumps({"comment": "Database error"}), 500

    elif request.method == "POST":  # inserimento prodotti
        logger.info(f"Richiesta > {request.data.decode()}")
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
            logger.critical(e.args[0])
            return json.dumps({"comment": "Database error"}), 500

    else:
        return 405, json.dumps({"comment": f"Method {request.method} not supported"})


@app.route("/newOrder", methods=["POST"])
def newOrder():
    """
    Gestisce la creazione di un nuovo ordine
    """
    logger = logging.getLogger("newOrder_log")

    token = request.headers.get('Authorizarion')
    logger.info(f"Token > {token}")
    validToken = _isValid_token(token)
    if validToken[0]:
        token = validToken[2]
        logger.debug(validToken[1])
    else:
        return json.dumps(validToken[1]), 401

    if request.method == "POST":
        if token['role'] != Roles.CUSTOMER.name:
            return json.dumps({"comment": "This user can't make new orders"}), 401

        logger.info(f"Ordine riceuto: {request.data.decode()}")
        logger.debug(f"isJson = {request.is_json}")
        try:
            if request.is_json:
                logger.debug(f"request.getjson() > {request.get_json()}")
                addInfo = {
                    "badge_n": token['badge_n'],
                    "role": token['role'],
                    "items": request.get_json()
                }
                response = OrdersManager().newOrder(addInfo)
                logger.info(f"Response > {response}. Type > {type(response)}")
                return json.dumps(response), 201
            else:
                return json.dumps({"comment": "No json provided"}), 400
        except DatabaseError as e:
            logger.critical(e.args[0])
            return json.dumps({"comment": "Database error"}), 500

    else:
        return json.dumps({"comment": f"Method {request.method} not supported"}), 405


@app.route("/registerCustomer", methods=["POST"])
def registerCustomer():
    """
    Permette la registrazione di un nuovo cliente
    """
    logger = logging.getLogger("registerCustomer_log")

    if request.method == "POST":
        logger.info(f"Registrazione nuovo cliente > {request.data.decode()}")
        try:
            if request.is_json:
                CustomersManager().addNewCustomer(request.get_json())
                return json.dumps({"comment": "Customer added"}), 201
            else:
                return json.dumps({"comment": "No json provided"}), 400
        except DatabaseError as e:
            logger.critical(e.args[0])
            return json.dumps({"comment": "Database error"}), 500
    else:
        return json.dumps({"comment": f"Method {request.method} not supported"}), 405


@app.route("/login", methods=["POST"])
def customerLogin():
    logger = logging.getLogger("login_log")

    if request.method == "POST":
        logger.info("Sent request: {request.data.decode()}")
        if request.is_json:
            response = AuthenticationManager().authenticateUser(request.get_json())
            return json.dumps(response), 200
        else:
            return json.dumps({"comment": "Credentials not provided"}), 400
    else:
        return json.dumps({"comment": f"Method {request.method} not supported"}), 500


@app.route("/payOrder", methods=["POST"])
def payOrder():
    logger = logging.getLogger("pay_log")

    token = request.headers.get('Authorizarion')
    logger.info(f"Token > {token}")
    validToken = _isValid_token(token)
    if validToken[0]:
        token = validToken[2]
        logger.info(validToken[1])
    else:
        return json.dumps(validToken[1]), 401

    if request.method == "POST":
        print("Incoming order summary:\n", request.data.decode())
        if request.is_json:
            response = PaymentsManager().pay(request.get_json())
            return json.dumps(response), 200
        else:
            return json.dumps({"comment": "No json provided"}), 400
    else:
        return json.dumps({"comment": f"Method {request.method} not supported"}), 405


@app.route("/trackOrder", methods=["GET"])
def trackOrder():
    logger = logging.getLogger("track_log")

    if request.method == "GET":
        trackingID = int(request.args.get('id'))
        logger.info("Tracking ID = ", trackingID)
        return json.dumps(ShippingsManager().trackOrder(trackingID)), 200


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