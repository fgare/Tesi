import psycopg2
import requests
import time
import random
from DBHandler import DBHandler


if __name__ == "__main__":
    while True:
        db = DBHandler()
        missingProducts = db.select("SELECT * FROM articles WHERE quantity <= 50;")

        for prod in missingProducts:
            n = random.randint(20,100)
            try:
                db.update(f"UPDATE articles SET quantity=quantity+{n} WHERE barcode={prod['barcode']};")
            except psycopg2.DatabaseError as dbe:
                print(dbe.args[0])

        db.close()
        time.sleep(5)
