from flask import Flask, render_template, request, redirect, url_for
from flask.helpers import flash
from static.API.currency import Currency
import datetime

app = Flask(__name__)
app.secret_key="aesavas"

c = Currency()
unit = c.currencyUnit

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
        date = request.form.get("date")
        if date == "":
            withdate = 0
            rates = c.latestConverter(fromMoney,toMoney)
        else:
            withdate = 1
            rates = c.historicalConverter(fromMoney,toMoney,date)
            date = datetime.datetime.strptime(date,'%Y-%m-%d').strftime("%d %B %Y")
        result = float(amount)*float(rates[toMoney])
        data = {
            "from":fromMoney,
            "to":toMoney,
            "rates":rates[toMoney],
            "amount":amount,
            "result":result,
            "date":date
        }
        return render_template("pages/converter.html", unit=unit, selected=1, data=data, withdate=withdate)
    else:
        return render_template("pages/converter.html", unit=unit)

@app.route("/rates",methods=["GET","POST"])
def allRates():
    if request.method == "POST":
        base = request.form.get("base")
        date = request.form.get("date")
        if date == "":
            apiData = c.latestRates(base)
        elif date < "1999-01-04":
            flash("Please do not choose older then 04-01-1999","warning")
            return render_template("pages/allrates.html", unit=unit)
        else:
            apiData = c.specialDateRates(base, date)
        data = {
            "date" : datetime.datetime.strptime(date,'%Y-%m-%d').strftime("%d %B %Y"),
            "base" : apiData["base"],
            "rates" : apiData["rates"]
        }
        return render_template("pages/allrates.html", unit=unit, data=data, selected=1)
    else:
        return render_template("pages/allrates.html", unit=unit)

