import argparse
import datetime
from urllib.parse import urlparse

from GoogleNews import GoogleNews
import mysql.connector
import urllib
import csv
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="stocks"
)

mycursor = mydb.cursor()

with open('HistoricalData_1690313502696.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in spamreader:
        parts = row[0].split(',')
        mtime = parts[0]
        dateparts = mtime.split("/")
        mtime = dateparts[2]+"-"+dateparts[0]+"-"+dateparts[1]
        query = f"""INSERT INTO `stocks`(`symbol`, `open`, `close`, `high`, `low`, `volume`, `date`) VALUES ('TSLA',{parts[3]},{parts[1]},{parts[4]},{parts[5]},{parts[2]},'{mtime}')"""
        mycursor.execute(query)
    mydb.commit()
        # Date,Close/Last,Volume,Open,High,Low