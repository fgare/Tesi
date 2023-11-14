from flask import Flask, request
import logging
import json
from psycopg2 import DatabaseError
from CustomersManager import CustomersManager


app = Flask(__name__)
loggingLevel = logging.CRITICAL  # livello di logging valido per tutto il progetto
logging.basicConfig(level=loggingLevel, format="%(asctime)s - %(levelname)s - %(message)s")


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


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5005, debug=True)