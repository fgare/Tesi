from flask import Flask, request
import logging
import json
from AuthenticationManager import AuthenticationManager


app = Flask(__name__)
loggingLevel = logging.CRITICAL  # livello di logging valido per tutto il progetto
logging.basicConfig(level=loggingLevel, format="%(asctime)s - %(levelname)s - %(message)s")


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


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)