import requests

class Currency():

    @staticmethod
    def getRequest(fromMoney, toMoney):
        basic_url = "https://api.exchangeratesapi.io/latest?"
        base = "base=" + fromMoney
        symbols = "symbols=" + toMoney
        current_url = basic_url + base + "&" + symbols
        return requests.get(current_url).json()["rates"]