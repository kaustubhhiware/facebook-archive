import argparse
import datetime
from datetime import timedelta
import json
import os
import sys
import dateutil.parser
import matplotlib.pyplot as plt
import numpy as np
from tabulate import tabulate
import timestring
import math

prog_desc = """
Plot your friends along the way.
Author - @kaustubhhiware
"""


def plot_friends_by_date(friends_list, weekwise = True):
    """plot_friends_by_date plots graphs with given friends data

    Arguments:
    - friend_list: a list of friend objects
    """
    if len(friends_list) == 0:
        print('No friends according to filters.')
        return

    dates = [timestring.Date(f['timestamp']).date for f in friends_list]
    dates.reverse()

    firstdate = dates[0]
    lastdate = dates[-1]
    maxdays = int((lastdate - firstdate).total_seconds() / 86400) + 1
    frndcount = [0] * int(maxdays)
    if weekwise:
        frndcount = [0]* math.ceil(maxdays / 7)
    monthwise = [0]*13
    # count number of friends each day, cumulative
    for i in range(len(dates)):
        days_diff = (dates[i] - firstdate).total_seconds() / 86400
        if weekwise:
            days_diff /= 7
        frndcount[int(days_diff)] += 1
        monthwise[dates[i].month] += 1

    xaxis = [lastdate - timedelta(days=i) for i in range(maxdays, 0, -1)]
    if weekwise:
        xaxis = xaxis[::7]
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
    plt.bar(xaxis, frndcount, label='New friends made each week', width=5)
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


def date_filter(friends, from_date, to_date):
    """ date_filter creates a list of friend objects
    which the friends are added between from_date and to_date

    Arguments:
    friends: a list of friend objects
    from_date: a timestring.Date instance or None
    to_date: a timestring.Date instance or None
    """
    if from_date is None and to_date is None:
        return friends

    if from_date and to_date:   # both are not None
        date_range = timestring.Range(start=from_date, end=to_date)
        # if timestamp in date_range is implemented by the timestring library
        return [f for f in friends if f['timestamp'] in date_range]

    # before to_date
    if from_date is None:
        return [f for f in friends if f['timestamp'] < to_date]
    # after from_date
    if to_date is None:
        return [f for f in friends if f['timestamp'] > from_date]

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=prog_desc)
    parser.add_argument('archive_path', metavar='PATH', type=str, nargs='?',
                        help='location of archive folder')
    parser.add_argument('--from', dest='from_date', type=str, default=None,
                        help='beginning time of plot (inclusive)')
    parser.add_argument('--to', dest='to_date', type=str, default=None,
                        help='ending time of plot (inclusive)')
    args = parser.parse_args()

    from_date = args.from_date
    if from_date is not None:
        try:
            from_date = timestring.Date(args.from_date)
        except:
            print('invalid --from date string')
            exit(1)

    to_date = args.to_date
    if to_date is not None:
        try:
            to_date = timestring.Date(args.to_date)
        except:
            print('invalid --to date string')
            exit(1)

    # check if arguments are valid
    if from_date and to_date and from_date > to_date:
        print('invalid --from --to range')
        exit(1)

    loc = args.archive_path
    if loc is None:
        loc = input('Enter facebook archive extracted location: ')
    loc = os.path.abspath(loc)
    if not os.path.isdir(loc):
        print("The provided location doesn't seem to be right")
        exit(1)

    fname = os.path.join(loc, 'friends/friends.json')
    if not os.path.isfile(fname):
        print("The file friends.json is not present at the entered location.")
        exit(1)

    with open(fname, 'r') as f:
        friends_json_str = f.read()

    data = json.loads(friends_json_str)
    friends_list = data['friends']

    if len(friends_list) == 0:
        print('You have 0 friends. No plots for you')
        exit(0)

    friends_list = date_filter(friends_list, from_date, to_date)
    plot_friends_by_date(friends_list)
