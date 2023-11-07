import datetime
import jwt

from MonolithicApp.Globals.DBHandler import DBHandler
from MonolithicApp.Globals import GlobalConstants
from MonolithicApp.Globals import Enumeratives

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
            return {"comment": "Login failed, wrong username or password", "token":None}

        # utente esiste
        user = user[0]
        if (user['email'] == credentials_json['email'] and
                user['password_hash'] == credentials_json['password']):  # email e password coincidono

            createdOn = datetime.datetime.now().replace(microsecond=0)
            expirity = createdOn + datetime.timedelta(minutes=30)

            payload = {
                "user": user['customerid'],
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
            return {"comment": "Login failed, wrong username or password", "token":None}


def checkToken(token) -> bool:
    """Decodifica il token JWT e verifica se esso è ancora valido o scaduto """
    try:
        decoded = jwt.decode(token, encryptionKey, encryptionAlgorithm)
    except jwt.exceptions.InvalidTokenError as ite:
        print("Invalid token supplied {%s}" % token)
        return False

    now = datetime.datetime.now()
    if decoded['expires'] > now:
        return True
    return False


if __name__ == "__main__":
# TODO: testare funzione chechtoken
