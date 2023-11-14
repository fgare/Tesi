import json
import psycopg2
import logging

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")


class DBHandler:

    def __init__(self):
        self._connection = self._connect()
        self._cursor = self._connection.cursor()

    def __del__(self):  # distruttore
        self._cursor.close()
        self._connection.close()

    def _connect(self):
        newConn = psycopg2.connect(
            host="localhost",
            database="supermercato",
            user="postgres",
            password="postgres",
            port=5433
        )
        logging.debug(f"DB connection > {newConn}")
        return newConn

    def select(self, query):
        logging.debug(f"Eseguo: {query}")
        try:
            self._cursor.execute(query)
            columns = [desc[0] for desc in self._cursor.description]
            result = [dict(zip(columns, row)) for row in self._cursor.fetchall()] # lista di dizionari
            return result
        except psycopg2.Error as e:
            raise e

    def update(self, query, response=False):
        logging.debug(f"Eseguo: {query}")
        try:
            self._cursor.execute(query)
            self._connection.commit()
            if response:
                return self._cursor.fetchall()
            else:
                return None
        except psycopg2.Error as e:
            logging.critical("Eseguo rollback")
            self._connection.rollback()
            raise e

    def commit(self):
        self._connection.commit()

    def close(self):
        self._cursor.close()
        self._connection.close()


# metodo main per test della classe
if __name__ == "__main__":
    mode = int(input("1. Select\n"
                    "2. Update\n"))

    db = DBHandler()
    if mode == 1:
        result = db.select("Select * from articles;")
        jsonResult = json.dumps(result)
        print(jsonResult)
    else:
        db.update("update articles set quantity = quantity + 5 where barcode in (1,9);")
        print("Done")
