import datetime

import psycopg2

from MonolithicApp.Globals.DBHandler import DBHandler
from MonolithicApp.Globals import GlobalConstants
from MonolithicApp.Globals import OrderState


class OrdersManager:

    def __init__(self):
        self.db = DBHandler()

    def newOrder(self, jsonOrder):
        # TODO: affinare, si può restituire un errore nel caso in cui la merce non sia presente in quantità sufficiente

        def calculatePrice(products):
            total = 0
            for element in products:
                getPrice_query = f"SELECT unit_price FROM {GlobalConstants.ARTICLES_DBTABLE} " \
                                 f"WHERE barcode = {element['barcode']};"
                result = self.db.select(getPrice_query)
                # print("Result= ", result)
                total += result[0]['unit_price'] * element['quantity']  # prezzo * quantità
            return total

        # creazione del nuovo ordine
        now = datetime.datetime.now().replace(microsecond=0)  # orario senza i microsecondi
        badge = jsonOrder["badge_n"]
        print("Badge_n = ", badge)
        createOrder_query = f"INSERT INTO {GlobalConstants.ORDERS_DBTABLE}(badge_n, orderdate, orderstate) " \
                            f"VALUES({badge}, '{now}', '{OrderState.OrderState.CREATED.name}') " \
                            f"RETURNING orderid;"
        orderID = self.db.update(createOrder_query, response=True)[0][0]
        print("Order ID = ", orderID)

        # aggiornamento quantità
        items = jsonOrder["items"]
        updateQuantities_query = ""
        for element in items:
            updateQuantities_query += f"UPDATE {GlobalConstants.ARTICLES_DBTABLE} " \
                                      f"SET quantity = quantity - {element['quantity']} " \
                                      f"WHERE barcode = {element['barcode']}; \n"

        # memorizza prodotti dell'ordine
        saveOrderItems_query = ""
        for element in items:
            saveOrderItems_query += f"INSERT INTO {GlobalConstants.ORDERITEMS_DBTABLE}(articleid, orderid, quantity) " \
                                    f"VALUES({element['barcode']}, {orderID}, {element['quantity']});\n"

        totalPrice = 0
        try:
            totalPrice = calculatePrice(items)
            self.db.update(updateQuantities_query + saveOrderItems_query)
            self.db.update(f"UPDATE {GlobalConstants.ORDERS_DBTABLE} SET total_price = {totalPrice} WHERE orderid = {orderID};")
        except psycopg2.Error as e:
            # se si genera un'eccezione devo cancellare anche l'ordine
            deleteOrder_query = f"DELETE FROM {GlobalConstants.ORDERS_DBTABLE} " \
                                f"WHERE orderID={orderID};"
            self.db.update(deleteOrder_query)
            print("Query error")

        return {
            "comment":"Order created",
            "badge_n": jsonOrder["badge_n"],
            "orderID": orderID,
            "orderState": OrderState.OrderState.CONFIRMED.name,
            "price": totalPrice
        }
