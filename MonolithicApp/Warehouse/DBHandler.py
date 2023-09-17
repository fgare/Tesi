import json

import psycopg2


class DBHandler:

    def __init__(self):
        self.connection = self._connect()
        # cursor = self.connection.cursor() rendere campo della classe

    def __del__(self): # distruttore
        self.connection.close()

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
        cursor = self.connection.cursor()
        cursor.execute(query)
        columns = [desc[0] for desc in cursor.description]
        result = [dict(zip(columns, row)) for row in cursor.fetchall()] # lista di dizionari
        return result

    def update(self, query):
        print("Eseguo: ", query)
        cursor = self.connection.cursor()
        result = cursor.execute(query)
        self.connection.commit()
        return result


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
