import json


class Customer:
    def __init__(self, csvString):
        splitted = csvString.split(',')
        self._id = splitted[0]
        self._surname = splitted[1].strip('"')
        self._badge = splitted[2]
        self._sex = splitted[3].strip('"')
        self._dob = splitted[4].strip('"')
        self._email = splitted[5].strip('"')
        self._password = splitted[6].strip('"')
        self._role = splitted[7].strip('"')

    def getCredentials(self):
        return {
            "email": self._email,
            "password": self._password
        }

    def toDict(self):
        return {
            "id": self._id,
            "surname": self._surname,
            "badge": self._badge,
            "sex": self._sex,
            "dob": self._dob,
            "email": self._email,
            "password": self._password,
            "role": self._role
        }

    def toString(self):
        return json.dumps(self.toDict())
