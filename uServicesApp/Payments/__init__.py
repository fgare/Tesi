from flask import Flask, request
import logging
import json
from PaymentsManager import PaymentsManager

app = Flask(__name__)
loggingLevel = logging.CRITICAL  # livello di logging valido per tutto il progetto
logging.basicConfig(level=loggingLevel, format="%(asctime)s - %(levelname)s - %(message)s")


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
    app.run(host='0.0.0.0', port=5003, debug=True)