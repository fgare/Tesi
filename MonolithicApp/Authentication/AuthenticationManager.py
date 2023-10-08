from MonolithicApp.Globals.DBHandler import DBHandler
from MonolithicApp.Globals import GlobalConstants


class AuthenticationManager:

    def __init__(self):
        self.db = DBHandler()

    def authenticateUser(self, credentials_json):
        checkUser_query = f"SELECT email, password_hash FROM {GlobalConstants.CUSTOMERS_DBTABLE} " \
                          f"WHERE email = '{credentials_json['email']}';"
        result = self.db.select(checkUser_query)

        if len(result) == 0:
            return {"comment": "Login failed, wrong username or password"}

        user = result[0]
        if (user['email'] == credentials_json['email'] and
            user['password_hash'] == credentials_json['password']):
            return {"comment": "Logged in"}
        else:
            return {"comment": "Login failed, wrong username or password"}
