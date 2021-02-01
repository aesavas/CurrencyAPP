from flask import Flask, render_template, request, redirect, url_for, make_response
from flask.helpers import flash
from static.API.currency import Currency
import datetime as dt
from static.API.download import Download

app = Flask(__name__)
app.secret_key="aesavas"

c = Currency()
d = Download()
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
            date = dt.datetime.strptime(str(dt.datetime.now().date()),'%Y-%m-%d').strftime("%d %B %Y")
            rates = c.latestConverter(fromMoney,toMoney)
        else:
            withdate = 1
            rates = c.historicalConverter(fromMoney,toMoney,date)
            date = dt.datetime.strptime(date,'%Y-%m-%d').strftime("%d %B %Y")
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
            date = dt.datetime.strptime(str(dt.datetime.now().date()),'%Y-%m-%d').strftime("%d %B %Y")
            apiData = c.latestRates(base)
        elif date < "1999-01-04":
            flash("Please do not choose older then 04-01-1999","warning")
            return render_template("pages/allrates.html", unit=unit)
        else:
            apiData = c.specialDateRates(base, date)
            date = dt.datetime.strptime(date,'%Y-%m-%d').strftime("%d %B %Y")
        data = {
            "date" : date,
            "base" : apiData["base"],
            "rates" : apiData["rates"]
        }
        return render_template("pages/allrates.html", unit=unit, data=data, selected=1)
    else:
        return render_template("pages/allrates.html", unit=unit)

@app.route("/historical-rates", methods=["GET","POST"])
def historicalRates():
    if request.method == "POST":
        fromMoney = request.form.get("base")
        toMoney = request.form.get("target")
        start = request.form.get("start")
        end = request.form.get("end")
        if start < "1999-01-04" or end < "1999-01-04":
            flash("Please do not choose older then 04-01-1999","warning")
            return render_template("pages/historicalrates.html", unit=unit)
        elif start > end:
            flash("Start date cannot newer then end date.","danger")
            return render_template("pages/historicalrates.html", unit=unit)
        else:
            apiData = c.dateRangeRates(fromMoney,toMoney,start,end)
            rates = {}
            for key, value in sorted(apiData["rates"].items()):
                rates[dt.datetime.strptime(key,'%Y-%m-%d').strftime("%d %B %Y")]=value[toMoney]
            data = {
                "base":fromMoney,
                "target":toMoney,
                "start":start,
                "end":end,
                "rates":rates
            }
            flash(f'{len(rates)} results found.','primary')
            return render_template("pages/historicalrates.html", unit=unit, selected=1, data=data)
    else:
        return render_template("pages/historicalrates.html", unit=unit)

@app.route("/downloads", methods=["GET","POST"])
def downloadsPage():
    if request.method == "POST":
        csv = ""
        filename = ""
        print(request.form)
        if len(request.form) == 2:
            base = request.form["base"]
            date = request.form["date"]
            if date == "":
                filename = dt.datetime.strptime(str(dt.datetime.now().date()),'%Y-%m-%d').strftime("%d %B %Y")
                csv = d.downloadLatestRates(base)
            elif date < "1999-01-04":
                flash("Please do not choose older then 04-01-1999","warning")
                return render_template("pages/downloads.html", unit=unit)
            else:
                csv = d.downloadSpecialDateRates(base, date)
                filename = dt.datetime.strptime(date,'%Y-%m-%d').strftime("%d %B %Y")
        else:
            fromMoney = request.form["fromMoney"]
            toMoney = request.form["toMoney"]
            start = request.form["start"]
            end = request.form["end"]
            if start < "1999-01-04" or end < "1999-01-04":
                flash("Please do not choose older then 04-01-1999","warning")
                return render_template("pages/downloads.html", unit=unit)
            elif start > end:
                flash("Start date cannot newer then end date.","danger")
                return render_template("pages/downloads.html", unit=unit)
            else:
                csv = d.downloadDateRangeDates(fromMoney,toMoney,start,end)
                start = dt.datetime.strptime(start,'%Y-%m-%d').strftime("%d %B %Y")
                end = dt.datetime.strptime(end,'%Y-%m-%d').strftime("%d %B %Y")
                filename = "StartAt-" + start + "EndAt-" + end
        filename += ".csv"
        response = make_response(csv)
        cd = f'attachment; filename={filename}'
        response.headers['Content-Disposition'] = cd 
        response.mimetype='text/csv'
        flash("Your data is downloaded !","danger")
        return response
    else:
        return render_template("pages/downloads.html", unit=unit)
