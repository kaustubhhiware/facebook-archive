import matplotlib.pyplot as plt
import os
import timestring
import datetime
from datetime import timedelta
import dateutil.parser
import numpy as np
import json
from tabulate import tabulate
import sys

"""
Plot your friends along the way.
Author - @kaustubhhiware
"""

today = datetime.datetime.now().strftime('%b %d, %y')
yesterday = (datetime.datetime.now() - timedelta(days=1)).strftime('%b %d, %y')

def friends(loc=""):
    if loc=="":
        loc = input('Enter facebook archive extracted location: ')
    if not os.path.isdir(loc):
        print("The provided location doesn't seem to be right")
        exit(1)
    
    fname = loc+'/friends/friends.json'
    if not os.path.isfile(fname):
        print("The file friends.json is not present at the entered location.")
        exit(1)

    with open(fname, 'r') as f:
        txt = f.read()
    
    data = json.loads(txt)
    
    dates = [timestring.Date(i["timestamp"]).date for i in data["friends"]]
    dates.reverse()
    
    firstdate = dates[0]    
    maxdays = int((dates[-1] - firstdate).total_seconds() / 86400) + 1
    frndcount = [0] * int(maxdays)
    monthwise = [0]*13
    # count number of friends each day, cumulative
    for i in range(len(dates)):
        days_diff = (dates[i] - firstdate).total_seconds() / 86400
        frndcount[int(days_diff)] += 1
        monthwise[dates[i].month] += 1
    
    xaxis = [ datetime.datetime.now() - timedelta(days=maxdays-i) for i in range(maxdays) ]
    cumulative_friends = np.cumsum(frndcount).tolist()

    print('Plotting new friends per day and cumulative friends')
    fig, ax = plt.subplots()
    ax2 = ax.twinx()
    ax.plot(xaxis, frndcount, color='C0', label='New each day')
    ax.set_ylabel('New each day')

    ax2.plot(xaxis, cumulative_friends, color='C1', label='Friends so far')
    ax2.set_ylabel('Friends so far')
    plt.legend(loc='upper left', ncol=2)
    plt.show()

    print('Plotting only new friends per day')
    plt.plot(xaxis, frndcount, label='New each day')
    plt.legend(loc='upper left', ncol=2)
    plt.show()

    print('Plotting monthwise friends')
    plt.plot(range(13), monthwise, label='per month')
    plt.legend(loc='upper left', ncol=2)
    plt.show()

    print('\nSome statistics based on the data: ')
    stats = []
    stats.append(["Total Friends", cumulative_friends[-1]])
    max_frnd_day = xaxis[frndcount.index(max(frndcount))]
    max_frnd_month = datetime.datetime(2000, monthwise.index(max(monthwise)), 1)
    stats.append(["Maximum Friends made on", max_frnd_day.date()])
    stats.append(["Maximum Friends made in month", max_frnd_month.strftime('%B')])
    print(tabulate(stats, headers=['Property', 'Value'], tablefmt='fancy_grid'))
    
if __name__ == '__main__':
    loc = ""
    if len(sys.argv) > 1:
        loc = sys.argv[1]
    friends(loc)
