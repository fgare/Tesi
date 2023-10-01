from enum import Enum


class OrderState(Enum):
    CREATED = 0
    PAID = 1
    CONFIRMED = 2
    ONDELIVERY = 3
    REFUSED = 4
    CANCELLED = 5
    DELIVERED = 6