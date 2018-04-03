import matplotlib.pyplot as plt
import os
import re
from copy import deepcopy
import timestring
import datetime
from datetime import timedelta
import dateutil.parser
import numpy as np

"""
Plot your friends along the way.
Author - @kaustubhhiware
"""

today = datetime.datetime.now().strftime('%b %d, %y')
yesterday = (datetime.datetime.now() - timedelta(days=1)).strftime('%b %d, %y')

def friends():
    loc = raw_input('Enter facebook archive extracted location: ')
    if not os.path.isdir(loc):
        print("The provided location doesn't seem to be right")
        exit(1)
    
    fname = loc+'/html/friends.htm'
    if not os.path.isfile(fname):
        print("File nahi hai yeh")
        print(1)

    with open(fname, 'r') as f:
        txt = f.readlines()
    txt = ''.join(txt)
    h2tags = [m.start() for m in re.finditer('<h2>', txt)]
    
    t = txt[h2tags[0]:h2tags[1]]
    t = t[ t.index('<ul>') + 4 : t.index('</ul>') ]
    t = t.split('</li>')
    t = filter(None, t)
    for i in range(len(t)):
        t[i] = t[i][4:-1]
        t[i] = t[i].split(' (')

    s = deepcopy(t)
    for i in range(len(s)):
        s[i][1] = timestring.Date(s[i][1])
        s[i][1] = s[i][1].date
    s.reverse()

    dates = [i[1] for i in s]
    firstdate = dates[0]
    for i in range(len(dates)):
        if dates[i] == 'Yesterday':
            dates[i] = yesterday
        elif dates[i] == 'Today':
            dates[i] = today
    maxdays = int((dates[-1] - firstdate).total_seconds() / 86400) + 1
    frndcount = [0] * int(maxdays)
    # count number of friends each day, cumulative
    for i in range(len(dates)):
        days_diff = (dates[i] - firstdate).total_seconds() / 86400
        frndcount[int(days_diff)] += 1
    xaxis = [ datetime.datetime.now() - timedelta(days=maxdays-i) for i in range(maxdays)  ]
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


if __name__ == '__main__':
    friends()
