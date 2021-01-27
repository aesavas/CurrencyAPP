from flask.globals import current_app
import requests

class Currency():

    def __init__(self):
        self.basic_url = "https://api.exchangeratesapi.io/"
        self.currencyUnit ={
            "EUR":"Euro",
            "USD":"US Dollar",
            "JPY":"Japanese Yen",
            "BGN":"Bulgarian Lev",
            "CZK":"Czech Koruna",
            "DKK":"Danish Koruna",
            "GBP":"Pound Sterling",
            "HUF":"Hungarian Forint",
            "PLN":"Polish Zloty",
            "RON":"Romanian Leu",
            "SEK":"Swedish Krona",
            "CHF":"Swiss Franc",
            "ISK":"Icelandic Krona",
            "NOK":"Norwegian Krone",
            "HRK":"Crotian Kuna",
            "RUB":"Russian Ruble",
            "TRY":"Turkish Lira",
            "AUD":"Australian Dollar",
            "BRL":"Brazilian Real",
            "CAD":"Canadian Dollar",
            "CNY":"Chinese Yuan",
            "HKD":"Hong Kong Dollar",
            "IDR":"Indonesian Rupian",
            "ILS":"Israeli Shekel",
            "INR":"Indian Rupee",
            "KRW":"South Korean Won",
            "MXN":"Mexican Peso",
            "MYR":"Malaysian Ringgit",
            "NZD":"New Zealand Dollar",
            "PHP":"Phillippine Peso",
            "SGD":"Singapore Dollar",
            "THB":"Thai Baht",
            "ZAR":"South African Rand"
        }

    def latestConverter(self,fromMoney, toMoney):
        
        base = "latest?base=" + fromMoney
        symbols = "symbols=" + toMoney
        current_url = self.basic_url + base + "&" + symbols
        return requests.get(current_url).json()["rates"]
    
    def historicalConverter(self,fromMoney, toMoney, date):
        base = "?base="+fromMoney
        symbols="&symbols="+toMoney
        current_url = self.basic_url + date + base + symbols
        return requests.get(current_url).json()["rates"]
    
    def latestRates(self, base):
        current_url = self.basic_url + "latest?base=" + base
        return requests.get(current_url).json()
    
    def specialDateRates(self, base, date):
        current_url = self.basic_url + date + "?base=" + base
        return requests.get(current_url).json()