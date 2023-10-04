import argparse
import datetime
from urllib.parse import urlparse
import traceback
from GoogleNews import GoogleNews
import mysql.connector
import urllib
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="stocks"
)
from gnews import GNews
import requests
from boilerpy3 import extractors


def getDataFromNews(url):
    try:
        y = requests.get(url)
        extractor = extractors.ArticleExtractor()
        try:
            content = extractor.get_content((y.content).decode('utf-8'))
            return content
        except:
            ex = traceback.format_exc()
        return y.content
    except:
        ex = traceback.format_exc()
        h=1
    return ""

def is_date_queried(date,symbol):
    mycursor = mydb.cursor()
    query = f"select count(*) as `count` from news where `date` = '{date}' and symbol='{symbol}'"
    mycursor.execute(query)
    num_news_found = int(mycursor.fetchall()[0][0])
    return num_news_found >= 3


def find_news(symbol, start_date, end_date, keywords):
    mycursor = mydb.cursor()
    if not is_date_queried(start_date,symbol):
        google_news = GNews()
        google_news.start_date = (start_date.year, start_date.month, start_date.day)  # Search from 1st Jan 2020
        google_news.end_date = (end_date.year, end_date.month, end_date.day)  # Search until 1st March 2020z
        news = google_news.get_news(" ".join(keywords))
        for result in news:
            try:
                datetime_object = datetime.datetime.strptime(result["published date"], '%a, %d %b %Y %H:%M:%S GMT')
                host = urlparse(result["publisher"]["href"]).hostname
                parsedTitle = str(result["title"]).replace("'", "")
                desc = getDataFromNews(result["url"])
                parsedDesc = str(desc).replace("'", "")

                try:
                    # todo: some dates are not in this format and fail
                    query = f"""replace INTO `news`(`link`, `host`, `title` ,`data`, `symbol`,`date`) VALUES ('{result["url"]}','{host}','{parsedTitle}','{parsedDesc}','{symbol}','{datetime_object.strftime('%Y-%m-%d %H:%M:%S')}')"""
                    mycursor.execute(query)
                    mydb.commit()
                except:
                    ex = traceback.format_exc()
                    g = 1
            except:
                ex = traceback.format_exc()
                h=1

        print(news[0])

def find_news2(symbol, start_date, end_date, keywords):
    mycursor = mydb.cursor()
    googlenews = GoogleNews(lang='en',encode='utf-8')
    googlenews.enableException(True)
    difference = end_date - start_date
    start_date_int = start_date
    end_date_int = start_date + datetime.timedelta(days=1)
    for now in range(difference.days):
        try:
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
                    ex = traceback.format_exc()
                    g=1
            mydb.commit()
            start_date_int = start_date_int + datetime.timedelta(days=1)
            end_date_int = end_date_int + datetime.timedelta(days=1)
        except:
            ex = traceback.format_exc()
            g=1

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
