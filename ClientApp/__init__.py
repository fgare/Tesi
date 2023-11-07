import json
import os
import csv
import linecache

import requests, datetime, random
from ClientApp.Customer import Customer

BASE = "http://127.0.0.1:5000/"
MAX = 100
CUSTOMER_MAX_ID = 2932
customers_fileName = "customers.csv"
token = ""
DEBUG = True


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
    requestHeader = {"authorization": token}
    return requests.get(BASE + "/productsList", headers=requestHeader)


if __name__ == "__main__":
    while True:
        # Eseguo continuamente il login con utenti diversi finchè uno non va a buon fine (in teoria subito)
        while True:
            selectedCustomer = randomSelectUser()
            loginSuccess = login(selectedCustomer)
            if loginSuccess[0]:
                token = loginSuccess[1]
                break

        # Richiedo elenco prodotti
        print("Productlist > ", productList())
