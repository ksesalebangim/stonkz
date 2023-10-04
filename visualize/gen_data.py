import argparse
import datetime
from datetime import datetime as dt
from urllib.parse import urlparse
import math
from GoogleNews import GoogleNews
import mysql.connector
import urllib
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import json
from visualize import getLowPassPoints, getPeaks
from news import find_news
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="stocks"
)

mycursor = mydb.cursor()
symbol = "TSLA"
mycursor.execute(
    f"SELECT  `close`,`date`  FROM `stocks` WHERE `symbol`='{symbol}' and date > '2019-05-00' order by `date` asc;")

myresult = mycursor.fetchall()
raw = []
raw_neg = []
values = []
peaks_raw = []
peaks_smoothed = []
peaks_smoothed_neg = []
dates = []
for x in myresult:
    values.append({"value": x[0], "date": x[1].strftime("%d.%m.%Y")})
    dates.append(x[1].strftime("%d.%m.%Y"))
    raw.append(x[0])
    raw_neg.append(-1*x[0])
    peaks_raw.append(None)
    peaks_smoothed.append(None)
    peaks_smoothed_neg.append(None)
smoothed = list(getLowPassPoints(raw))
smoothed_neg = list(getLowPassPoints(raw_neg))
peaks = list(getPeaks(raw))
for el in peaks:
    peaks_raw[el] = raw[el]

peaks = list(getPeaks(smoothed))
for el in peaks:
    peaks_smoothed[el] = smoothed[el]

peaks = list(getPeaks(smoothed_neg))
for el in peaks:
    peaks_smoothed_neg[el] = smoothed[el]


for x in range(len(values)):
    values[x]["smoothed"] = smoothed[x]
    values[x]["peaks"] = peaks_raw[x]
    values[x]["peaks_smoothed"] = peaks_smoothed[x]
    values[x]["peaks_smoothed_neg"] = peaks_smoothed_neg[x]









asValues = json.dumps(values)

f = open("chartjs/src/acquisitions_proto.js", "r")
template = str(f.read())
f.close()
template = template.replace("/*replace_me*/", asValues)


f = open("chartjs/src/acquisitions.js", "w")
f.write(template)
f.close()
for x in range(len(peaks_smoothed)):
    if peaks_smoothed[x] is not None:
        print(dates[x])
        datetime_object = dt.strptime(dates[x], '%d.%m.%Y')
        #find_news(symbol,datetime_object,datetime_object+datetime.timedelta(days=10),["tesla"])
for x in range(len(peaks_smoothed_neg)):
    if peaks_smoothed[x] is not None:
        print(dates[x])