import json

from DBHandler import DBHandler
from Globals import GlobalConstants


class WarehouseManager:

    def __init__(self):
        self.db = DBHandler()

    def getProductsList(self):
        query = f"SELECT * FROM {GlobalConstants.ARTICLES_DBTABLE};"
        return self.db.select(query)

    def getProductQuantity(self, productName):
        query = f"SELECT * FROM {GlobalConstants.ARTICLES_DBTABLE} WHERE name = '{productName}';"
        return self.db.select(query)

    def addProduct(self, jsonString):
        def prepareQuery(element: dict):
            query = f"UPDATE {GlobalConstants.ARTICLES_DBTABLE} " \
                    f"SET quantity = quantity + {element['quantity']} " \
                    f"WHERE barcode = {element['barcode']};"
            return DBHandler().update(query)

        if isinstance(jsonString, list):
            for d in jsonString: # scorre la lista di dizionari
                prepareQuery(d)
        else:
            prepareQuery(jsonString) # c'è un solo dizionario
