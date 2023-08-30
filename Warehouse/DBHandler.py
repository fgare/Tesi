import psycopg2

class DBHandler:

    def __int__(self):
        self.connection = self._connect()

    def __del__(self): #distruttore
        self.connection.close()

    def _connect(self):
        connection = psycopg2.connect(
            host = "localhost",
            database = "supermercato",
            user = "postgres",
            password = "postgres",
            port = 5433
        )
        print("Connection > ", connection)

    def execute(self, query):
        cursor = self.connection.cursor()
        return cursor.execute(query)