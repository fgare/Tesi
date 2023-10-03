import datetime

from MonolithicApp.Globals.DBHandler import DBHandler
from MonolithicApp.Globals import GlobalConstants
import json

class OrdersManager:

    def __init__(self):
        self.db = DBHandler()

    def newOrder(self, jsonOrder):
        # creazione del nuovo ordine
        now = datetime.datetime.now()
        badge = jsonOrder["badge_n"]
        print("Badge_n = ", badge)
        createOrder_query = f"INSERT INTO {GlobalConstants.ORDERS_DBTABLE}(badge_n, orderdate) " \
                            f"VALUES({badge}, '{now}') " \
                            f"RETURNING orderid;"
        orderID = self.db.update(createOrder_query, False)
        print("Order ID = ", orderID)

        # aggiornamento quantità
        items = jsonOrder["items"]
        updateQuantities_query = ""
        for element in items:
            updateQuantities_query += f"UPDATE {GlobalConstants.ARTICLES_DBTABLE} " \
                                    f"SET quantity = quantity - {element['quantity']} " \
                                    f"WHERE barcode = {element['barcode']};\n"
        self.db.update(updateQuantities_query, False)

        # memorizza prodotti nell'ordine
        saveOrderItems_query = ""
        for element in items:
            saveOrderItems_query += f"INSERT INTO {GlobalConstants.ORDERITEMS_DBTABLE} " \
                                f"({element['barcode']}, {orderID}, {element['quantity']});\n"
        self.db.update(saveOrderItems_query, False)

        self.db.commit()

