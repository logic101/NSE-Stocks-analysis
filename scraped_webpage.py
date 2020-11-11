import requests
from bs4 import BeautifulSoup
import csv
import datetime
import time
import schedule
import dash


app = dash.Dash('__name__')
server = app.server


def csv_file():
    # Use requests to load the webpage
    webpage = requests.get('https://afx.kwayisi.org/nseke/')

    # Create the beautiful soup object
    obj = BeautifulSoup(webpage.content, 'lxml')

    # get the trades table
    table = obj.find_all(attrs={'class': 't'})
    table = table[1]

    # Get the stock prices
    price = table.find_all(attrs={'class': 'r'})
    prices = []
    for i in price[2:]:
        p = i.get_text()
        prices.append(p)
    for i in prices:
        if '+' in i or '-' in i or '__' in i:
            prices.remove(i)

    # Company's names
    company = table.find_all(attrs={'class': 'n'})
    companies = []
    for c in company:
        co = c.get_text()
        companies.append(co)

    # Tickers column
    marker = table.find_all('a')
    tickers = []
    for m in marker:
        ma = m.get_text()
        tickers.append(ma)
    for ticker in tickers:
        if len(ticker) > 8:
            tickers.remove(ticker)

    # Create today's dates
    date = datetime.date.today()
    # Now create the csv file that data will be loaded to
    field_names = ['ticker', 'company', 'price', 'date']

    def write_csv():
        with open('pg4_data.csv', 'a', newline='') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=field_names)
            for t, c, p in zip(tickers, companies, prices):
                info = {
                    'ticker': t,
                    'company': c,
                    'price': p,
                    'date': date

                }

                csv_writer.writerow(info)

    schedule.every().day.at('21:47').do(write_csv)
    while True:
        schedule.run_pending()
        time.sleep(1)


csv_file()
if __name__ == '__main__':
    app.run_server(debug=True, port=700)
