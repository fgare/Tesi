import json


class Article:
    def __init__(self, barcode, name, quantity):
        self.barcode = barcode
        self.name = name
        self.quantity = quantity

    def __str__(self):
        return f"({self.barcode}, {self.name}, {self.quantity})"

    """Restituisce un dizionario con il valore dei campi dell'oggetto"""
    def toDict(self):
        return {
            "barcode": self.barcode,
            "name": self.name,
            "quantity": self.quantity
        }

    """Crea un'istanza di Article partendo da un json in cui sono specificati i valori dei campi dell'oggetto"""
    @classmethod
    def parse(cls, jsonString):
        data = json.loads(jsonString)
        barcode = data.get("barcode")
        name = data.get("name")
        quantity = data.get("quantity")
        return cls(barcode, name, quantity)


#main per test
if __name__ == "__main__":
    newObj = {
        "barcode": 5,
        "name": "apples",
        "quantity": 60
    }
    obj_json = json.dumps(newObj)
    realObj = Article.parse(obj_json)
    print(f"{realObj} \n{realObj.toDict()}")