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

def getLowPassPoints(points):
    points_orig = np.array(points)
    points_out = low_pass_filter(points_orig,15,500)
    return points_out

def getPeaks(points):
    points_peaks, _ = signal.find_peaks(points,rel_height=0.1)
    return points_peaks