import json
import os
import linecache

import requests
import random
from MonolithicApp.Globals.Customer import Customer
from MonolithicApp.Globals.Article import Article

BASE = "http://127.0.0.1:5000/"
MAXITEMS = 100  # Dimensione massima del carrello
N_OF_ARTICLES = 168  # numero di differenti articoli nel magazzino
CUSTOMER_MAX_ID = 2932  # Numero di clienti registrati
MAX_PURCHASABLE = 10  # Numero massimo di pezzi acquistabili per ogni prodotto
customers_fileName = "customers.csv"
token = ""
DEBUG = True

"""
Come procedere:
1. Login e ottengo il token
2. Elenco prodotti
3. Scelgo prodotti e quantità
4. Genero un nuovo ordine
5. Pago ordine
"""


def randomSelectUser():
    """
    Legge il file con tutti i clienti e ne seleziona uno a caso
    :return: Oggetto Customer
    """
    currentDirectory = os.getcwd()
    customer_filePath = os.path.join(currentDirectory, customers_fileName)

    with open(customer_filePath, 'r', newline=""):
        lineNumber = random.randint(2, CUSTOMER_MAX_ID)
        line = linecache.getline(customer_filePath, lineNumber)
        if DEBUG: print("Selected line = ", line)
        return Customer(line)


def login(customer):
    reply = requests.post(BASE + "/login", json=customer.getCredentials())
    if DEBUG: print(f"Status Code = {reply.status_code}\nBody = {reply.text}")

    if reply.status_code == 200:
        body = json.loads(reply.text)
        return True, body['token']
    else:
        return False, None


def productList():
    """
    Richiede la lista di prodotti
    :return: Status code della richiesta e una lista di dizionari con i prodotti
    """
    requestHeader = {"Authorization": token}
    response = requests.get(BASE + "/productsList", headers=requestHeader)

    # considera ogni dizionario corrispondente a un prodotto e lo converte nell'oggetto Article
    products = json.loads(response.text)
    articles = []
    for el in products:
        articles.append(Article.parse(el))

    return response.status_code, articles


def fillCart(products) -> set:
    cart = set()
    numberOfItems = random.randint(1, 15)  # sorteggia il numero di prodotti da inserire nel carrello
    for i in range(numberOfItems):
        drawnProduct = random.randint(0, len(products)-1)  # sorteggia un prodotto da inserire nel carrello
        drawnQuantity = random.randint(1, MAX_PURCHASABLE)  # sorteggia la quantità di prodotto da acquistare
        choosenProd = products.pop(drawnProduct)  # rimuove e ritorna l'elemento nella posizione specificata
        choosenProd.quantity = drawnQuantity
        cart.add(choosenProd)
    return cart


def set_to_dict(cart: set) -> list:
    articlesList = []
    while cart:
        elem = cart.pop()
        articlesList.append(elem.toDict())
    return articlesList


if __name__ == "__main__":
    for _ in range(100):
        # Eseguo continuamente il login con utenti diversi finché uno non va a buon fine (in teoria subito)
        while True:
            selectedCustomer = randomSelectUser()
            loginSuccess = login(selectedCustomer)
            if DEBUG: print("Login success > ", loginSuccess)
            if loginSuccess[0]:
                token = loginSuccess[1]
                break

        products = productList()[1]  # Richiedo elenco prodotti, ottengo lista di Articles
        if DEBUG: print(f"Received {len(products)} products. ", end='')
        cart = fillCart(products)  # riempi il carrello, ritorna un set di Articles
        if DEBUG: print(f"Cart dimension = {len(cart)}")

        # genero nuovo ordine
        response = requests.post(
            url=BASE + "/newOrder",
            headers={"Authorizarion": token, "Content-Type": "application/json"},
            data=json.dumps(set_to_dict(cart))
        )

        if DEBUG: print((response.status_code,response.text) if response.status_code==201 else response.status_code)
        orderInfo = json.loads(response.text)

        response = requests.post(
            url=BASE+"/payOrder",
            headers={"Authorizarion": token, "Content-Type": "application/json"},
            data=json.dumps({"orderID":orderInfo['orderID']})
        )
        if DEBUG: print((response.status_code,response.text) if response.status_code==201 else response.status_code)

        print("Order shipped")

