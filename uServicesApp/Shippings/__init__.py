from flask import Flask, request
import logging
import json
from ShippingManager import ShippingsManager


app = Flask(__name__)
loggingLevel = logging.CRITICAL  # livello di logging valido per tutto il progetto
logging.basicConfig(level=loggingLevel, format="%(asctime)s - %(levelname)s - %(message)s")

@app.route("/trackOrder", methods=["GET"])
def trackOrder():
    logger = logging.getLogger("track_log")

    if request.method == "GET":
        trackingID = int(request.args.get('id'))
        logger.info("Tracking ID = ", trackingID)
        return json.dumps(ShippingsManager().trackOrder(trackingID)), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5004, debug=True)