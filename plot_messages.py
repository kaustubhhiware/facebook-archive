import matplotlib.pyplot as plt
import os
import re
from copy import deepcopy
import timestring
import datetime
from datetime import timedelta
import dateutil.parser
import numpy as np
import argparse

def loop_messages(loc):

    osfiles = [f for f in os.listdir(loc+'/messages/') if os.path.isfile(loc+'/messages/'+f)]
    with open('temp.html','w') as outfile:
        for file in osfiles:
            with open(loc + '/messages/' + file, 'r') as infile:
                txt = infile.readlines()
                txt = filter(None, txt)
                outfile.writelines(txt)
    messages(loc, loop=True, fname='temp.html')


def messages(loc, loop=False, toplot=True,m_id=-1, fname=''):
    if not loop:    
        m_id = raw_input("Enter id for friend: ")
        m_id = int(m_id)
        # m_id=511
        fname = loc+'/messages/'+ str(m_id) + '.html'

    if not os.path.isfile(fname):
        print("File nahi hai yeh "+fname)
        print(1)

    with open(fname, 'r') as f:
        txt = f.readlines()
    txt = ''.join(txt)
    metastart = [m.start() for m in re.finditer('<span class="meta">', txt)]
    metaend = [m.start() for m in re.finditer('UTC', txt)]

    if len(metaend) > len(metastart):
        metaend = metaend[0:len(metastart)]

    d = [txt[ metastart[i]+19 : metaend[i] ] for i in range(len(metastart)) ]
    d = filter(None, d)
    d2 = [dateutil.parser.parse(i) for i in d]
    d2.reverse()

    first = min(d2)
    maxhours = int((max(d2) - first).total_seconds() / 3600) + 1
    msgcount = [0] * int(maxhours)
    # count number of friends each day, cumulative
    for i in range(len(d2)):
        hours_diff = (d2[i] - first).total_seconds() / 3600
        msgcount[int(hours_diff)] += 1
    xaxis = [ datetime.datetime.now() - timedelta(hours=maxhours-i) for i in range(maxhours)  ]
    cumulative_msgs = np.cumsum(msgcount).tolist()

    monthwise, hourwise = [0]*13, [0]*25
    for i in range(len(d2)):
        monthwise[d2[i].month] += 1
        hourwise[d2[i].hour] += 1

    if toplot:
        print('Plotting new messages per hour and cumulative messages')
        fig, ax = plt.subplots()
        ax2 = ax.twinx()
        ax.plot(xaxis, msgcount, color='C0', label='New each hour')
        ax.set_ylabel('New each hour')

        ax2.plot(xaxis, cumulative_msgs, color='C1', label='Messages so far')
        ax2.set_ylabel('Messages so far')
        plt.legend(loc='upper left', ncol=2)
        plt.show()

        print('Plotting only new messages per hour')
        plt.plot(xaxis, msgcount, label='New each hour')
        plt.legend(loc='upper left', ncol=2)
        plt.show()

        print('Plotting monthwise messages')
        plt.plot(range(13), monthwise, label='per month')
        plt.legend(loc='upper left', ncol=2)
        plt.show()

        print('Plotting only new messages per hour')
        plt.plot(range(25), hourwise, label='New each hour')
        plt.legend(loc='upper left', ncol=2)
        plt.show()

    return msgcount, cumulative_msgs, monthwise, hourwise


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--all', action='store_true', help="Display all users and groups messages")
    args = parser.parse_args()

    loc = raw_input('Enter facebook archive extracted location: ')
    if not os.path.isdir(loc):
        print("The provided location doesn't seem to be right")
        exit(1)
    if args.all:
        loop_messages(loc)
    else:
        messages(loc)
