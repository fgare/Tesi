from flask import Flask, request
import logging
import json
from psycopg2 import DatabaseError
from OrdersManager import OrdersManager
from Globals.Enumeratives import Roles
from AuthenticationManager import checkToken


app = Flask(__name__)
loggingLevel = logging.CRITICAL  # livello di logging valido per tutto il progetto
logging.basicConfig(level=loggingLevel, format="%(asctime)s - %(levelname)s - %(message)s")

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
    app.run(host='0.0.0.0', port=5002, debug=True)