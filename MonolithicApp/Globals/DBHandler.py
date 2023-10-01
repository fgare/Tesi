import json

import psycopg2


class DBHandler:

    def __init__(self):
        self._connection = self._connect()
        self._cursor = self._connection.cursor()

    def __del__(self): # distruttore
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
        print("Connection > ", newConn)
        return newConn

    def select(self, query):
        self._cursor.execute(query)
        columns = [desc[0] for desc in self._cursor.description]
        result = [dict(zip(columns, row)) for row in self._cursor.fetchall()] # lista di dizionari
        return result

    def update(self, query, autocommit = True):
        print("Eseguo: ", query)
        result = self._cursor.execute(query)
        if autocommit: self._connection.commit()
        return result

    def commit(self):
        self._connection.commit()


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
