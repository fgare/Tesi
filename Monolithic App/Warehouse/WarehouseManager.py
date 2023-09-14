from DBHandler import DBHandler
import GlobalConstants


class WarehouseManager:

    def __init__(self):
        self.db = DBHandler()

    def getProductsList(self):
        query = f"SELECT * FROM {GlobalConstants.ARTICLES_DBTABLE};"
        return self.db.execute(query)

    def getProductQuantity(self, productName):
        query = f"SELECT * FROM {GlobalConstants.ARTICLES_DBTABLE} WHERE name = '{productName}';"
        return self.db.execute(query)

    def addProduct(self, jsonString):
        query = f"UPDATE {GlobalConstants.ARTICLES_DBTABLE} SET quantity=5 WHERE name =;"
        #TODO: continua
