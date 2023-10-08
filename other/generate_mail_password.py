import psycopg2
import secrets
import string
import hashlib
import csv
import os

def generatePassword(length):
    characters = string.ascii_letters + string.digits
    password = "".join(secrets.choice(characters) for _ in range(length))
    return password

customers_path = 'customersTable_backup.csv'
customers_path = os.path.join(os.path.dirname(__file__), customers_path)
dati = []
with open(customers_path) as csv_file:
    lettore = csv.reader(csv_file, delimiter=',')

    for riga in lettore:
        dati.append(riga)

# print(dati)

conn = psycopg2.connect(
            host="localhost",
            database="supermercato",
            user="postgres",
            password="postgres",
            port=5433
        )
print("Connection > ", conn)
cursor = conn.cursor()

for row in dati:
    password = row[6]
    sha3 = hashlib.sha3_256()
    sha3.update(password.encode('utf-8'))
    password = sha3.hexdigest()
    query = f"UPDATE customers " \
            f"SET password = '{password}' " \
            f"WHERE customerid = {row[0]};"
    print(query)
    cursor.execute(query)
    

conn.commit()
cursor.close
conn.close

