import random

import psycopg2
import time
import random

from Globals.DBHandler import DBHandler
from Globals import GlobalConstants
from Globals.Enumeratives import OrderState


class PaymentsManager:

    def __init__(self):
        self.db = DBHandler()

    def pay(self, jsonSummary):
        orderID = jsonSummary["orderID"]
        checkOrder_query = f"SELECT total_price, orderstate FROM {GlobalConstants.ORDERS_DBTABLE} " \
                           f"WHERE orderid={orderID};"
        try:
            orderSummary = self.db.select(checkOrder_query)
        except psycopg2.Error as e:
            return {
                "comment": "Database error"
            }
        orderSummary = orderSummary[0]  # estrae l'unico elemento presente nella lista

        if not orderSummary['orderstate'] == OrderState.CONFIRMED.name:
            return {
                "comment": "It is impossible to pay this order"
            }

        time.sleep(0.1)  # thread dorme per 100 ms, simula pagamento

        # Nel 10% dei casi il pagamento viene rifiutato
        if random.random() < 0.1:
            updateOrderState_query = f"UPDATE {GlobalConstants.ORDERS_DBTABLE} " \
                                     f"SET orderstate ='{OrderState.REFUSED.name}' " \
                                     f"WHERE orderid={orderID};"
            self.db.update(updateOrderState_query)
            print(f"Order ID={orderID} has been refused")

            return {
                "comment": f"Your order has been refused",
                "orderID": orderID,
                "orderState": OrderState.REFUSED.name,
                "price": None
            }

        # pagamento accettato
        updateOrderState_query = f"UPDATE {GlobalConstants.ORDERS_DBTABLE} " \
                                 f"SET orderstate='{OrderState.PAID.name}' " \
                                 f"WHERE orderid={orderID};"
        self.db.update(updateOrderState_query)
        print(f"Order ID={orderID} has been paid")

        return {
            "comment": f"Order successfully paid (€ {str(orderSummary['total_price'])})",
            "orderID": orderID,
            "orderState": OrderState.PAID.name,
            "price": float(orderSummary['total_price'])
        }
