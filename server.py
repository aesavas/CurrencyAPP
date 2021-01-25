from flask import Flask, render_template, request, redirect, url_for
from static.API.currency import Currency


app = Flask(__name__)

unit = {
    "GBP":"British Pound",
    "TRY":"Turkish Liras",
    "USD":"American Dollar"
}



@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/converter",methods=["GET","POST"])
def converter():
    if request.method == "POST":
        fromMoney = request.form.get("from")
        toMoney = request.form.get("to")
        amount = request.form.get("amount")
        rates = Currency.getRequest(fromMoney,toMoney)
        print(rates)
        result = float(amount)*float(rates[toMoney])
        data = {
            "from":fromMoney,
            "to":toMoney,
            "rates":rates[toMoney],
            "amount":amount,
            "result":result
        }
        return render_template("pages/converter.html", unit=unit, selected=1, data=data)
    else:
        return render_template("pages/converter.html", unit=unit)