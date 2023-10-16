from MonolithicApp.Globals.DBHandler import DBHandler
from MonolithicApp.Globals.Enumeratives import OrderState
from MonolithicApp.Globals import GlobalConstants


class ShippingsManager:

    def __init__(self):
        self.db = DBHandler()

    def trackOrder(self, id):
        selectOrder_query = f"SELECT orderstate " \
                            f"FROM {GlobalConstants.ORDERS_DBTABLE} " \
                            f"WHERE orderid = {id};"
        result = self.db.select(selectOrder_query)
        if len(result) == 0:
            return {
                "comment": "Order not found"
            }

        return {
            "orderID": id,
            "orderState": result[0]['orderstate']
        }

    def shipOrder(self, jsonOrder):
        updateState_query = f"UPDATE {GlobalConstants.ORDERS_DBTABLE} " \
                            f"SET orderstate = '{OrderState.ONDELIVERY.name}' " \
                            f"WHERE orderid = {jsonOrder['orderID']};"
        self.db.update(updateState_query)
        print("Order {ID = {0}} is on the way".format(jsonOrder['orderID']))

        return {
            "comment": "Order is on the way",
            "orderID": jsonOrder['orderID'],
            "orderState": OrderState.ONDELIVERY.name
        }