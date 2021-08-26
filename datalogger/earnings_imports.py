import csv
import pandas
import datetime
import time
from yahoo_earnings_calendar import YahooEarningsCalendar


def query_earnings_syms_and_print_to_csv(syms_list, filename):
    with open(filename, 'w', newline='') as file:
        fieldnames = ['Stock', 'Q1 2017 date', 'Q1 2017 Est', 'Q1 2017 Act', 'Q2 2017 date', 'Q2 2017 Est', 'Q2 2017 Act',
                        'Q3 2017 date', 'Q3 2017 Est', 'Q3 2017 Act','Q4 2017 date', 'Q4 2017 Est', 'Q4 2017 Act',
                        'Q1 2018 date', 'Q1 2018 Est', 'Q1 2018 Act','Q2 2018 date', 'Q2 2018 Est', 'Q2 2018 Act',
                        'Q3 2018 date', 'Q3 2018 Est', 'Q3 2018 Act','Q4 2018 date', 'Q4 2018 Est', 'Q4 2018 Act'] 
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for sym in syms_list:
            listEarning = []
            listDates = [] #we have "doubles" on dates, because the time is 00:00 and then 21:00 or 19:00, values are the same
            earnings = yec.get_earnings_of(sym)
            for datepoint in earnings:
                convertedDate = datetime.datetime.strptime(datepoint['startdatetime'] , '%Y-%m-%dT%H:%M:%S.%fZ')
                if date_from <= convertedDate <= date_to :
                    dayMonthYear = convertedDate.date() #.date() to not get hour, min,sec
                    if dayMonthYear not in listDates:
                        listDates.append(dayMonthYear) 
                        listEarning.append({
                            "Date" : convertedDate,
                            "Est": datepoint['epsestimate'],
                            "Act": datepoint['epsactual']
                        })
            print(sym)
        #testons combien ne marchent pas
            if len(listEarning) >= 8:
                #at this point expecting to have every earning for 1 sym, can append row to csv
                #output is ordered, most recent to less recent
                writer.writerow({'Stock': sym, 
                    'Q1 2017 date':listEarning[7]['Date'], 'Q1 2017 Est':listEarning[7]['Est'], 'Q1 2017 Act':listEarning[7]['Act'], 
                    'Q2 2017 date':listEarning[6]['Date'], 'Q2 2017 Est':listEarning[6]['Est'], 'Q2 2017 Act':listEarning[6]['Act'],
                    'Q3 2017 date':listEarning[5]['Date'], 'Q3 2017 Est':listEarning[5]['Est'], 'Q3 2017 Act':listEarning[5]['Act'],
                    'Q4 2017 date':listEarning[4]['Date'], 'Q4 2017 Est':listEarning[4]['Est'], 'Q4 2017 Act':listEarning[4]['Act'],
                    'Q1 2018 date':listEarning[3]['Date'], 'Q1 2018 Est':listEarning[3]['Est'], 'Q1 2018 Act':listEarning[3]['Act'],
                    'Q2 2018 date':listEarning[2]['Date'], 'Q2 2018 Est':listEarning[2]['Est'], 'Q2 2018 Act':listEarning[2]['Act'],
                    'Q3 2018 date':listEarning[1]['Date'], 'Q3 2018 Est':listEarning[1]['Est'], 'Q3 2018 Act':listEarning[1]['Act'],
                    'Q4 2018 date':listEarning[0]['Date'], 'Q4 2018 Est':listEarning[0]['Est'], 'Q4 2018 Act':listEarning[0]['Act'] })
            else:
                print("sym out")


if __name__ == '__main__':

    yec = YahooEarningsCalendar()
        
    date_from = datetime.datetime.strptime('Jan 1 2017  01:00AM', '%b %d %Y %I:%M%p')
    date_to = datetime.datetime.strptime('Dec 31 2018  11:00PM', '%b %d %Y %I:%M%p')

    data = pandas.read_csv('data/companies.csv', names=None)
    sym_list = data.Symbols.tolist()

    #list of syms not retrievable with yahoo finance
    missing_sym_list = ["APC", "ARNC", "BBT", "BHGE", "CBS", "CELG", "DOW", "DWDP",
                "FOX", "FOXA", "HCP", "HRS", "JEC", "LEN", "LLL", "NWS", "RHT", "SYMC", "TMK", "TSS", "VIAB", "WCG"]

    filename = "data/earnings_" + time.strftime("%Y%m%d-%H%M%S") + ".csv"

    query_earnings_syms_and_print_to_csv(sym_list, filename)

    

# TODO
# complete missing earnings
# clean code
