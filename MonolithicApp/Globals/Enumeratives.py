from enum import Enum


class OrderState(Enum):
    CREATED = 0  # Ordine è stato ricevuto
    PAID = 1  # Ordine è stato pagato
    CONFIRMED = 2  # Ogni prodotto all'interno dell'ordine è presente nel magazzino in quantità sufficiente, l'ordine può quindi essere evaso
    ONDELIVERY = 3  # Ordine in consegna (spedito)
    REFUSED = 4  # Ordine rifiutato, almeno un prodotto non è presente in quantità sufficiente
    CANCELLED = 5  # Ordine cancellato dal cliente
    DELIVERED = 6  # Ordine consegnato


class TokenState(Enum):
    VALID = 0
    EXPIRED = 1


class Roles(Enum):
    CUSTOMER = 0  # Utente che può generare ordini
    SUPPLIER = 1  # Utente che può aggiungere prodotti al magazzino
