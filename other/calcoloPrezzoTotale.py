import psycopg2

def calculatePrice(products):
    total = 0
    for element in products:
        getPrice_query = f"SELECT unit_price FROM articles " \
                        f"WHERE barcode = {element['barcode']};"
        print("Eseguo > ", getPrice_query)
        cursor.execute(getPrice_query)
        result = cursor.fetchall()
        print("Result > ", result[0][0])
        total += result[0][0] * element['quantity']  # prezzo * quantità
    return total

conn = psycopg2.connect(
            host="localhost",
            database="supermercato",
            user="postgres",
            password="postgres",
            port=5433
        )

cursor = conn.cursor()

request = {
    "badge_n": 6,
    "order_id": None,
    "items": [
        {
            "barcode":1,
            "name":"fragole",
            "quantity":5
        },
        {
            "barcode":28,
            "name":"cofee",
            "quantity":2
        }
    ]
}

items = request['items']

total = calculatePrice(items)
print("Total = ", total)
