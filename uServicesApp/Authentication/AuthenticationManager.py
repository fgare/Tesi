import datetime
import json

import jwt

from Globals.DBHandler import DBHandler
from Globals import GlobalConstants

encryptionKey = "insubria"
encryptionAlgorithm = "HS256"

class AuthenticationManager:

    def __init__(self):
        self.db = DBHandler()

    def authenticateUser(self, credentials_json):
        """
        Genera un nuovo token per l'utente
        """
        # cerca tutte le informazioni dell'utente sulla base della mail
        checkUser_query = f"SELECT * FROM {GlobalConstants.CUSTOMERS_DBTABLE} " \
                          f"WHERE email = '{credentials_json['email']}';"
        user = self.db.select(checkUser_query)

        # utente non esiste, ho una lista vuota
        if len(user) == 0:
            return {"comment": "Login failed, wrong username or password", "token": None}

        # utente esiste
        user = user[0]
        if (user['email'] == credentials_json['email'] and
                user['password_hash'] == credentials_json['password']):  # email e password coincidono

            createdOn = datetime.datetime.now().replace(microsecond=0)
            expirity = createdOn + datetime.timedelta(minutes=30)

            payload = {
                "badge_n": user['badge_n'],
                "created": createdOn.strftime("%Y-%m-%d %H:%M:%S"),
                "expires": expirity.strftime("%Y-%m-%d %H:%M:%S"),
                "role": user['customerrole']
            }

            # cripta il token utilizzando la chiave
            encoded = jwt.encode(payload, encryptionKey, encryptionAlgorithm)

            return {
                "comment": "Login succeded",
                "token": encoded
            }
        else:
            return {"comment": "Login failed, wrong username or password", "token": None}


def checkToken(token):
    """Decodifica il token JWT e verifica se esso è ancora valido o scaduto """
    decoded = None
    try:
        decoded = jwt.decode(token, encryptionKey, encryptionAlgorithm)
        print("Decoded token > ", decoded)
    except jwt.exceptions.InvalidTokenError as ite:
        print("Invalid token supplied {%s}" % token)
        return False

    now = datetime.datetime.now()
    expiration = datetime.datetime.strptime(decoded['expires'], "%Y-%m-%d %H:%M:%S")

    if expiration > now:
        return True, decoded
    return False, None


if __name__ == "__main__":
    credentials = {
        "email": "Young@example.com",
        "password": "a659d44b0a12d28b906ddc2cc3222053af4eb4d56a67bb3d1ce33acc495f67a3"
    }
    auth_token = AuthenticationManager().authenticateUser(credentials)
    token = auth_token['token']

    decoded = checkToken(token)
    print("Encoded token > ", token, "\nCheck > ", decoded[0], "\nDecoded > ", decoded[1])
