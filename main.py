import argparse
import datetime
from urllib.parse import urlparse

from GoogleNews import GoogleNews
import mysql.connector
import urllib
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="stocks"
)


def find_news(symbol, start_date, end_date, keywords):
    mycursor = mydb.cursor()
    googlenews = GoogleNews(lang='en',encode='utf-8')
    googlenews.enableException(True)
    difference = end_date - start_date
    start_date_int = start_date
    end_date_int = start_date + datetime.timedelta(days=1)
    for now in range(difference.days):
        googlenews.set_time_range(start=start_date_int.strftime("%m/%d/%Y"),end=end_date_int.strftime("%m/%d/%Y"))
        keywordsSTR = ' '.join(keywords)
        googlenews.search(keywordsSTR)
        resultsPage = googlenews.results()
        for result in resultsPage:
            host = urlparse(result["link"]).hostname
            parsedTitle = str(result["title"]).replace("'","")
            parsedDesc = str(result["desc"]).replace("'", "")
            try:
                #todo: some dates are not in this format and fail
                query = f"""replace INTO `news`(`link`, `host`, `title` ,`data`, `symbol`,`date`) VALUES ('{result["link"]}','{host}','{parsedTitle}','{parsedDesc}','{symbol}','{result["datetime"].strftime('%Y-%m-%d %H:%M:%S')}')"""
                mycursor.execute(query)
            except:
                g=1
        mydb.commit()
        start_date_int = start_date_int + datetime.timedelta(days=1)
        end_date_int = end_date_int + datetime.timedelta(days=1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='sticks',
        description='What the program does',
        epilog='Text at the bottom of help')
    parser.add_argument("--symbol", type=str)
    parser.add_argument('--start', type=lambda s: datetime.datetime.strptime(s, '%d/%m/%Y'))
    parser.add_argument("--end", type=lambda s: datetime.datetime.strptime(s, '%d/%m/%Y'))
    parser.add_argument("--keywords", nargs="+", type=str)
    args = parser.parse_args()
    find_news(args.symbol, args.start, args.end, args.keywords)
