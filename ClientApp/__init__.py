import json

import requests, datetime, random

BASE = "http://127.0.0.1:5000/"
MAX = 100
CUSTOMER_MAX_ID = 2932

if __name__ == "__main__":
    while True:
        # sorteggia cliente
        customerID = random.randint(1,CUSTOMER_MAX_ID)

        # richiedi elenco prodotti
        products = requests.get(BASE + "productsList")
        products = json.loads(products.json())
        # print("Products >\n", products.json())
        print(f"product = ", products[0])
        shoppingCartDimension = random.randint(5, 200)  # numero di prodotti da inserire nel carrello
        productsNumber = len(products)  # numero di prodotti in magazzino
        items_in_cart = []  # articoli aggiunti al carrello

        for _ in range(0, shoppingCartDimension):
            choosenProd = random.choice(products)  # seleziona casualmente un prodotto
            prodQuantity = choosenProd['quantity']
            getQuantity = random.randint(1, 0.8 * choosenProd['quantity'])  # preleva una quantità tra 1 e l'80% della disponibilità

            items_in_cart.append({
                "barcode": choosenProd['barcode'],
                "quantity": getQuantity
            })

    # compone il json di richiesta
    jsonRequest = {
        "badge_n": customerID,
        "order_id": None,
        "items": items_in_cart
    }
    newOrderResponse = requests.post(BASE + "newOrder", jsonRequest)
    print(newOrderResponse)