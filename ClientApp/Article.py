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
    def parse(cls, data):
        if isinstance(data, str):
            data = json.loads(data)  # converto in dizionario
        # A questo punto il tipo deve essere dict, altrimenti viene restituita un'eccezione
        if not isinstance(data, dict):
            raise TypeError("The type provided must be str or dict")
        return cls(
            data['barcode'],
            data['name'],
            data['quantity']
        )

    def __str__(self):
        return f"{{Barcode: {self.barcode}, Name: {self.name}, Quantity: {self.quantity}}}"


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
    print(realObj)