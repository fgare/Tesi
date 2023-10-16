import datetime

from MonolithicApp.Globals.DBHandler import DBHandler
from MonolithicApp.Globals import GlobalConstants
from MonolithicApp.Globals import Enumeratives


class AuthenticationManager:

    def __init__(self):
        self.db = DBHandler()

    def authenticateUser(self, credentials_json):
        # cerca tutte le informazioni dell'utente sulla base della mail
        checkUser_query = f"SELECT * FROM {GlobalConstants.CUSTOMERS_DBTABLE} " \
                          f"WHERE email = '{credentials_json['email']}';"
        user = self.db.select(checkUser_query)
        # print("Result > ", user)

        # utente non esiste
        if len(user) == 0:
            return {"comment": "Login failed, wrong username or password"}

        # utente esiste
        user = user[0]
        if (user['email'] == credentials_json['email'] and
                user['password_hash'] == credentials_json['password']):  # email e password coincidono

            # Vengono marcati come scaduti tutti gli eventuali token ancora validi
            # (La query potrebbe anche non modificare alcuna tupla)
            switchTokenState_query = f"UPDATE {GlobalConstants.LOGINS_DBTABLE} " \
                                     f"SET loginstate = '{Enumeratives.TokenState.EXPIRED.name}' " \
                                     f"WHERE customerid = {user['customerid']} AND " \
                                     f"(loginstate = '{Enumeratives.TokenState.VALID.name}' OR expirity < now());"
            self.db.update(switchTokenState_query)

            # l'utente necessita di un nuovo token
            createdOn = datetime.datetime.now().replace(microsecond=0)
            expirity = createdOn + datetime.timedelta(minutes=10)
            # print("Created on = ", createdOn)
            # print("Expirity = ", expirity)

            # genero un nuovo token
            newToken_query = f"INSERT INTO {GlobalConstants.LOGINS_DBTABLE} (createdon, expirity, customerid) " \
                             f"VALUES ('{createdOn}', '{expirity}', {user['customerid']}) " \
                             f"RETURNING tokenid;"
            tokenID = self.db.update(newToken_query, response=True)[0][0]

            return {
                "comment": "Logged in",
                "tokenID": tokenID,
                "valid_until": expirity.strftime("%Y-%m-%d %H:%M:%S"),
                "role": user['customerrole']
            }
        else:
            return {"comment": "Login failed, wrong username or password"}
