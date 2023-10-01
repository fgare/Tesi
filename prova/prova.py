from flask import Flask, request

app = Flask(__name__)


@app.route("/productsList", methods=["GET","POST"])
def productList():
    if request.method == "GET":
        return "Ci sei riuscito!"
    elif request.method == "POST":
        if request.is_json:
            return "x"
        else:
            return "xx"


if __name__ == "__main__":
    app.run(debug=True)