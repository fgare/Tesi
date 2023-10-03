from MonolithicApp.Globals.DBHandler import DBHandler
from MonolithicApp.Globals import GlobalConstants


class CustomersManager:

    def __init__(self):
        self.db = DBHandler()

    def addNewCustomer(self, jsonString):
        query = f"INSERT INTO {GlobalConstants.CUSTOMERS_DBTABLE}(surname,sex,dob) " \
                f"VALUES('{jsonString['surname']}', '{jsonString['sex']}', '{jsonString['dob']}');"
        self.db.update(query)
