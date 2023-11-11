import datetime

import psycopg2

from MonolithicApp.Globals.DBHandler import DBHandler
from MonolithicApp.Globals import GlobalConstants
from MonolithicApp.Globals import Enumeratives


class OrdersManager:

    def __init__(self):
        self.db = DBHandler()

    def newOrder(self, jsonOrder):
        def calculatePrice(products):
            """
            Calcola il prezzo totale di un carrello della spesa.
            :param products: Lista di prodotti
            :return: Prezzo totale
            """
            total = 0
            for element in products:
                getPrice_query = f"SELECT unit_price FROM {GlobalConstants.ARTICLES_DBTABLE} " \
                                 f"WHERE barcode = {element['barcode']};"
                result = self.db.select(getPrice_query)
                # print("Result= ", result)
                total += result[0]['unit_price'] * element['quantity']  # prezzo * quantità
            return round(total, 2)

        # creazione del nuovo ordine
        now = datetime.datetime.now().replace(microsecond=0)  # orario senza i microsecondi
        badge = jsonOrder["badge_n"]
        print("Badge_n = ", badge)
        createOrder_query = f"INSERT INTO {GlobalConstants.ORDERS_DBTABLE}(badge_n,orderdate,orderstate) " \
                            f"VALUES({badge},'{now}','{Enumeratives.OrderState.CREATED.name}') " \
                            f"RETURNING orderid;"
        orderID = self.db.update(createOrder_query, response=True)[0][0]
        print("Order ID = ", orderID)

        # imposta lo stato dell'ordine su CONFERMATO
        self.db.update(f"UPDATE {GlobalConstants.ORDERS_DBTABLE} "
                       f"SET orderstate='{Enumeratives.OrderState.CONFIRMED.name}' "
                       f"WHERE orderid={orderID};")

        # aggiornamento quantità
        items = jsonOrder["items"]
        updateQuantities_query = ""
        for element in items:
            updateQuantities_query += f"UPDATE {GlobalConstants.ARTICLES_DBTABLE} " \
                                      f"SET quantity = quantity-{element['quantity']} " \
                                      f"WHERE barcode={element['barcode']}; \n"

        # memorizza prodotti dell'ordine
        saveOrderItems_query = ""
        for element in items:
            saveOrderItems_query += f"INSERT INTO {GlobalConstants.ORDERITEMS_DBTABLE}(articleid,orderid,quantity) " \
                                    f"VALUES ({element['barcode']},{orderID},{element['quantity']});\n"

        totalPrice = 0
        try:
            totalPrice = calculatePrice(items)
            # In un'unica transazione modifica la quantità residua di ogni prodotto e
            # memorizza l'ordine (prodotti acquistati e relativa quantità)
            self.db.update(updateQuantities_query + saveOrderItems_query)
            # Salva il prezzo totale dell'ordine
            self.db.update(
                f"UPDATE {GlobalConstants.ORDERS_DBTABLE} SET total_price={totalPrice} WHERE orderid={orderID};")
        except psycopg2.Error as e:
            # se si genera un'eccezione devo cancellare anche l'ordine
            cancelOrder_query = f"UPDATE {GlobalConstants.ORDERS_DBTABLE} " \
                                f"SET orderstate = '{Enumeratives.OrderState.CANCELLED.name}' " \
                                f"WHERE orderID={orderID};"
            self.db.update(cancelOrder_query)
            if e.pgcode == "2200":
                print("Insufficient quantity")
            else:
                print("Query error")
            # Restituisce un json indicante l'errore
            return {
                "comment": "Order cancelled",
                "badge_n": jsonOrder["badge_n"],
                "orderID": orderID,
                "orderState": Enumeratives.OrderState.CANCELLED.name,
                "price": totalPrice
            }

        return {
            "comment": "Order created",
            "badge_n": jsonOrder["badge_n"],
            "orderID": orderID,
            "orderState": Enumeratives.OrderState.CONFIRMED.name,
            "price": totalPrice
        }
