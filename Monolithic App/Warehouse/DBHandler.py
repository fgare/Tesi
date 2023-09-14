import json

import psycopg2

class DBHandler:

    def __init__(self):
        self.connection = self._connect()

    def __del__(self): #distruttore
        self.connection.close()

    def _connect(self):
        newConn = psycopg2.connect(
            host = "localhost",
            database = "supermercato",
            user = "postgres",
            password = "postgres",
            port = 5433
        )
        print("Connection > ", newConn)
        return newConn

    def execute(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        columns = [desc[0] for desc in cursor.description]
        result = [dict(zip(columns, row)) for row in cursor.fetchall()] #lista di dizionari
        return result


#metodo main per test della classe
if __name__ == "__main__":
    db = DBHandler()
    result = db.execute("Select * from articles;")
    jsonResult = json.dumps(result,indent=4)
    print(jsonResult)

