import psycopg2
import time

from MonolithicApp.Globals.DBHandler import DBHandler
from MonolithicApp.Globals import GlobalConstants
from MonolithicApp.Globals.OrderState import OrderState


class PaymentsManager:

    def __init__(self):
        self.db = DBHandler()

    def pay(self, jsonSummary):
        orderID = jsonSummary["orderID"]
        checkOrder_query = f"SELECT total_price, orderstate FROM {GlobalConstants.ORDERS_DBTABLE} " \
                           f"WHERE orderid = {orderID};"
        try:
            orderSummary = self.db.select(checkOrder_query)
        except psycopg2.Error as e:
            return {
                "comment": "Unrecognized order ID"
            }
        orderSummary = orderSummary[0]  # estrae l'unico elemento presente nella lista

        if not orderSummary['orderstate'] == OrderState.CREATED.name:
            return {
                "comment": "It is impossible to pay this order"
            }

        time.sleep(0.1)  # thread dorme per 100 ms, simula pagamento

        # aggiorna lo stato dell'ordine
        updateOrderState_query = f"UPDATE {GlobalConstants.ORDERS_DBTABLE} " \
                                 f"SET orderstate = '{OrderState.PAID.name}' " \
                                 f"WHERE orderid = {orderID};"
        self.db.update(updateOrderState_query)
        print(f"Order ID={orderID} has been paid")

        return {
            "comment": f"Order successfully paid (€ {str(orderSummary['total_price'])})",
            "orderID": orderID,
            "orderState": OrderState.PAID.name,
            "price": float(orderSummary['total_price'])
        }
