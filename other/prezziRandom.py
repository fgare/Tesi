''' 
Script per il popolamento automatico della colonna prezzi della tabella 'articles'.
Vengono assegnati valori casuali nell'intervallo [0.5, 10]
'''

import psycopg2
import random
import datetime

conn = psycopg2.connect(
            host="localhost",
            database="supermercato",
            user="postgres",
            password="postgres",
            port=5433
        )

cursor = conn.cursor()
conn.autocommit = False

start = datetime.datetime.now()
count = 1
while True:
    price = random.random() * (10-0.5) + 0.5
    price = round(price, 2)
    try:
        query = f"UPDATE articles SET unit_price = {price} WHERE barcode = {count};"
        print("Eseguo: ", query)
        cursor.execute(query)
    except psycopg2.Error as e:
        break
    count += 1
    if count > 200:
        break

end = datetime.datetime.now()
tempo = end - start

conn.commit()
print(f"Completato, modificate {count} righe\nImpiegato {tempo}")

cursor.close()
conn.close()