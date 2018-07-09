import matplotlib.pyplot as plt
import os
import timestring
import datetime
from datetime import timedelta
import dateutil.parser
import numpy as np
import json
from tabulate import tabulate
from matplotlib.font_manager import FontProperties




today = datetime.datetime.now().strftime('%b %d, %y')
yesterday = (datetime.datetime.now() - timedelta(days=1)).strftime('%b %d, %y')



def friends():
    loc = input('Enter facebook archive extracted location: ')
    if not os.path.isdir(loc):
        print("The provided location doesn't seem to be right")
        exit(1)
    
    rname = loc+'/friends/received_friend_requests.json'
    fname = loc+'/friends/friends.json'
    sname = loc+'/friends/sent_friend_requests.json'

    if not os.path.isfile(fname):
        print("The file friends.json is not present at the entered location.")
        exit(1)

    with open(fname, 'r') as f:
        txt = f.read()

    with open(rname,'r') as r:
    	rtxt = r.read()

    with open(sname,'r') as s:
    	stxt = s.read()

    data = json.loads(txt)
    dates = [timestring.Date(i["timestamp"]).date for i in data["friends"]]
    dates.reverse()

    firstdate = dates[0]    
    maxdays = int((dates[-1] - firstdate).total_seconds() / 86400) + 1
    frndcount = [0] * int(maxdays)
    maxmonth = maxdays/30 +1
    monthwise = [0]*int(maxmonth)

    rdata = json.loads(rtxt)
    rdates = [timestring.Date(i["timestamp"]).date for i in rdata["received_requests"]]
    rdates.reverse()

    rfirstdate = rdates[0]    
    rmaxdays = int((rdates[-1] - rfirstdate).total_seconds() / 86400) + 1
    rfrndcount = [0] * int(rmaxdays)
    rmaxmonth= rmaxdays/30 +1
    rmonthwise = [0]*int(rmaxmonth)


    sdata = json.loads(stxt)
    sdates = [timestring.Date(i["timestamp"]).date for i in sdata["sent_requests"]]
    sdates.reverse()

    sfirstdate = sdates[0]    
    smaxdays = int((sdates[-1] - sfirstdate).total_seconds() / 86400) + 1
    sfrndcount = [0] * int(smaxdays)
    smaxmonth = smaxdays/30 +1
    smonthwise = [0]*int(smaxmonth)
 	   
    for i in range(len(dates)):
        days_diff = (dates[i] - firstdate).total_seconds() / 86400
        frndcount[int(days_diff)] += 1
        month_diff = int((dates[i] - firstdate).total_seconds()/2592000)
        monthwise[month_diff] += 1
    xaxis = [ datetime.datetime.now() - timedelta(days=maxdays-i) for i in range(maxdays) ]
    cumulative_friends = np.cumsum(frndcount).tolist()
    
    for i in range(len(rdates)):
        rdays_diff = (rdates[i] - rfirstdate).total_seconds() / 86400
        rfrndcount[int(rdays_diff)] += 1
        rmonth_diff = int((rdates[i] - rfirstdate).total_seconds() / 2592000)
        rmonthwise[rmonth_diff] += 1
    rxaxis = [ datetime.datetime.now() - timedelta(days=rmaxdays-i) for i in range(rmaxdays) ]
    rcumulative_friends = np.cumsum(rfrndcount).tolist()

    
    for i in range(len(sdates)):
        sdays_diff = (sdates[i] - sfirstdate).total_seconds() / 86400
        sfrndcount[int(sdays_diff)] += 1
        smonth_diff = int((sdates[i] - sfirstdate).total_seconds() / 2592000)
        smonthwise[smonth_diff] += 1

    sxaxis = [ datetime.datetime.now() - timedelta(days=smaxdays-i) for i in range(smaxdays) ]
    scumulative_friends = np.cumsum(sfrndcount).tolist()
    print('Plotting new friends per day ')
    fig, ax = plt.subplots()
    ax.plot(xaxis, frndcount,color = 'r',label = 'TotalFriend')
    ax.plot(rxaxis, rfrndcount,color = 'b',label = 'ReceivedFriendRequest')
    ax.plot(sxaxis,sfrndcount,color = 'g',label = 'SentFriendRequest')
    legend = ax.legend(loc='upper left')
    ax.set_ylabel('New each day')
    ax.set_xlabel('Year')
    plt.show()
    l= min(len(rmonthwise),len(smonthwise))
    overall = [0]*l
    percentage_recieved_friend = [0]*l
    percentage_send_friend_request = [0]*l

    for i in range(l):
        if rmonthwise[i]==0:
            percentage_recieved_friend[i]=0
            percentage_send_friend_request[i] = 100
        else:

            percentage_recieved_friend[i] = (rmonthwise[i]/(rmonthwise[i]+smonthwise[i]))*100
            percentage_send_friend_request[i] = 100-(percentage_recieved_friend[i])


    xind = np.arange(len(rmonthwise))
    width = 0.8
    print('Plotting percentage of send and received friends request')
    p1 = plt.bar(xind, percentage_recieved_friend, width)#received_freind_request
    p2 = plt.bar(xind, percentage_send_friend_request, width,
                 bottom=percentage_recieved_friend)
    plt.ylabel('Total Friends Request Send Or received')
    plt.title('Facebook Friends')
    plt.xticks(xind,fontsize=5)
    plt.legend((p1[0], p2[0]),('ReceivedFriendRequest','SentFriendRequest'))
    plt.show()

if __name__ == '__main__':
    friends()
