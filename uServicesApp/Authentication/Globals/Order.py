import json

from MonolithicApp.Globals.Enumeratives import OrderState

class Order:
    def __init__(self, id:int, state:OrderState, badge:int, price:int):
        self._id = id
        self._state = state
        self._customerBadge = badge
        self._price = price

    def toDict(self):
        return {
            "id": self._id,
            "state": self._state.name,
            "badge": self._customerBadge,
            "price": self._price
        }

    @classmethod
    def parse(cls, data):
        if isinstance(data, str):
            data = json.loads(data)
        if not isinstance(data, dict):
            raise TypeError("The type provided must be str or dict")

        return cls(
            data['id'],
            data['state'],
            data['badge'],
            data['price']
        )

    def __str__(self):
        return f"{{Order ID={self._id}, State={self._state.name}, Badge={self._customerBadge}, Price={self._price}}}"
