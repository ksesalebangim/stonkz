import argparse
import datetime
from urllib.parse import urlparse
import math
from GoogleNews import GoogleNews
import mysql.connector
import urllib
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal


def get_local_max(myarr,start_index,size):
    localMax = myarr[start_index]
    localmaxIndex = start_index
    for x in range(size):
        index = max(start_index -size + x,0)
        if localMax < myarr[index]:
            localMax = myarr[index]
            localmaxIndex = index
    return localmaxIndex

def get_local_min(myarr,start_index,size):
    localMax = myarr[start_index]
    localmaxIndex = start_index
    for x in range(size):
        index = max(start_index -size + x,0)
        if localMax > myarr[index]:
            localMax = myarr[index]
            localmaxIndex = index
    return localmaxIndex
def low_pass_filter(data, band_limit, sampling_rate):
    cutoff_index = int(band_limit * data.size / sampling_rate)
    F = np.fft.fft(data)
    F[cutoff_index + 1 : -cutoff_index] = 0
    return np.fft.ifft(F).real

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="stocks"
)

mycursor = mydb.cursor()
symbol = "TSLA"
mycursor.execute(
    f"SELECT  `close`,`date`  FROM `stocks` WHERE `symbol`='{symbol}' order by `date` asc;")

myresult = mycursor.fetchall()
points = []
for x in myresult:
    points.append(x[0])
points_orig = arr = np.array(points)
points = low_pass_filter(points_orig,17,1000)
negPoints = points * -1
points_peaks_neg, _ = signal.find_peaks(negPoints)
points_peaks, _ = signal.find_peaks(points)
promin = signal.peak_prominences(points, points_peaks)[0]
contur_height = points[points_peaks] - promin
#filter = np.max(points[points_peaks])
#points_peaks_filter = points[points_peaks] > filter*0.1
#points_peaks = points_peaks[points_peaks_filter]

#filter_neg = np.min(negPoints[points_peaks_neg])
#points_peaks_filter_neg = negPoints[points_peaks_neg] < filter_neg*0.1
#points_peaks_neg = points_peaks_neg[points_peaks_filter_neg]

#for x in range(len(points_peaks_neg)):
points_peaks_neg2 = [x for x in points_peaks_neg if x not in points_peaks]
points_peaks = [x for x in points_peaks if x not in points_peaks_neg]
points_peaks_neg = points_peaks_neg2
sums = []
for x in range(len(points_peaks)):
    sums.append(points[points_peaks[x]]-points[points_peaks_neg[x]])
sums = arr = np.array(sums)



maxSums = np.max(sums)
filter = sums > maxSums*0.3
xx = []
yy = []
for x in range(len(filter)):
    if filter[x]:
        xx.append(points_peaks[x])
        yy.append(points_peaks_neg[x])
points_peaks = np.array(xx)
points_peaks_neg = np.array(yy)
plt.plot(points_orig)

points_peaks_max = []
points_peaks_neg_min = []
for x in range(len(points_peaks)):
    xx = get_local_max(points_orig,points_peaks[x],30)
    points_peaks_max.append(xx)

for x in range(len(points_peaks_neg)):
    xx = get_local_min(points_orig,points_peaks_neg[x],30)
    points_peaks_neg_min.append(xx)


plt.plot(points_peaks_max, points_orig[points_peaks_max], "*")
plt.plot(points_peaks_neg_min, points_orig[points_peaks_neg_min], "*")

for x in points_peaks:
    print(myresult[x])

for x in points_peaks_neg:
    print(myresult[x])
#plt.plot(np.zeros_like(points_peaks), "--", color="green")"""
#plt.plot(points_orig)

plt.plot(points)
#plt.vlines(x=points_peaks, ymin=contur_height, ymax=points[points_peaks])
plt.show()