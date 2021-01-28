import datetime as dt
from static.API.currency import Currency


class Download():

    def __init__(self):
        self.c = Currency()

    def downloadLatestRates(self, base):
        latestRates = self.c.latestRates(base)
        csvFile = "Base,Abbreviation,Currency Unit,Rate\n"
        for key,value in latestRates["rates"].items():
            print(key, value)
            csvFile += f'{base},{key},{self.c.currencyUnit[key]},{value}\n'
        return csvFile
    
    def downloadSpecialDateRates(self,base,date):
        specialDateRates = self.c.specialDateRates(base, date)
        csvFile = "Base,Abbreviation,Currency Unit,Rate\n"
        for key,value in specialDateRates["rates"].items():
            csvFile += f'{base},{key},{"" if self.c.currencyUnit.get(key) is None else self.c.currencyUnit[key]},{value}\n'
        return csvFile

    def downloadDateRangeDates(self, base, target, start_at, end_at):
        dateRangeRates = self.c.dateRangeRates(base,target,start_at, end_at)
        csvFile = "Date,Base,Abbreviation,Currency Unit,Rate\n"
        for key,value in sorted(dateRangeRates["rates"].items()):
            csvFile += f'{dt.datetime.strptime(key,"%Y-%m-%d").strftime("%d %B %Y")},{base},{target},{self.c.currencyUnit.get(target)},{value[target]}\n'
        return csvFile
