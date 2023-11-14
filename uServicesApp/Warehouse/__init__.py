from flask import Flask, request
import logging
import json
from psycopg2 import DatabaseError
from WarehouseManager import WarehouseManager
from AuthenticationManager import checkToken
from Globals.Enumeratives import Roles


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
    app.run(host='0.0.0.0', port=5001, debug=True)