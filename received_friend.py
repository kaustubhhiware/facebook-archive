import matplotlib.pyplot as plt
import os
import timestring
import datetime
from datetime import timedelta
import dateutil.parser
import numpy as np
import json
from tabulate import tabulate
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
    monthwise = [0]*13   
    
    sdata = json.loads(stxt)
    sdates = [timestring.Date(i["timestamp"]).date for i in sdata["sent_requests"]]
    sdates.reverse()
    sfirstdate = sdates[0]    
    smaxdays = int((sdates[-1] - sfirstdate).total_seconds() / 86400) + 1
    sfrndcount = [0] * int(smaxdays)
    smonthwise = [0]*13
    
    rdata = json.loads(rtxt)
    rdates = [timestring.Date(i["timestamp"]).date for i in rdata["received_requests"]]
    rdates.reverse()
    rfirstdate = rdates[0]    
    rmaxdays = int((rdates[-1] - rfirstdate).total_seconds() / 86400) + 1
    rfrndcount = [0] * int(rmaxdays)
    rmonthwise = [0]*13
    
    for i in range(len(dates)):
        days_diff = (dates[i] - firstdate).total_seconds() / 86400
        frndcount[int(days_diff)] += 1
        monthwise[dates[i].month] += 1
    xaxis = [ datetime.datetime.now() - timedelta(days=maxdays-i) for i in range(maxdays) ]
    cumulative_friends = np.cumsum(frndcount).tolist()

    for i in range(len(rdates)):
        rdays_diff = (rdates[i] - rfirstdate).total_seconds() / 86400
        rfrndcount[int(rdays_diff)] += 1
        rmonthwise[rdates[i].month] += 1
    rxaxis = [ datetime.datetime.now() - timedelta(days=rmaxdays-i) for i in range(rmaxdays) ]
    rcumulative_friends = np.cumsum(rfrndcount).tolist()
    
    for i in range(len(sdates)):
        sdays_diff = (sdates[i] - sfirstdate).total_seconds() / 86400
        sfrndcount[int(sdays_diff)] += 1
        smonthwise[sdates[i].month] += 1
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

    print('Plotting monthwise friends')
    fig,ax=plt.subplots()
    ax.plot(range(13), monthwise,color = 'b',label ='TotalFriend')
    ax.plot(range(13),rmonthwise, color= 'r',label = 'ReceivedFriendRequest')
    ax.plot(range(13),smonthwise,color = 'g',label = 'SentFriendRequest')
    legend = ax.legend(loc='upper left')
    plt.title('Monthwise')
    plt.show()
    percentage_received_friend = [0]*13
    percentage_send_friend_request = [0]*13
    for i in range(13):
        if rmonthwise[i]==0:
            percentage_received_friend[i]=0
            percentage_send_friend_request[i] = 100
        else:
            percentage_received_friend[i] = (rmonthwise[i]/(rmonthwise[i]+smonthwise[i]))*100
            percentage_send_friend_request[i] = 100-(percentage_received_friend[i])

    xind = np.arange(13)
    width = 0.35
    print('Plotting percentage of send and received friends request')
    p1 = plt.bar(xind, percentage_received_friend, width)#received_freind_request
    p2 = plt.bar(xind, percentage_send_friend_request, width,
                 bottom=percentage_received_friend)

    plt.ylabel('Total Friends Request Send Or received')
    plt.title('Facebook Friends')
    plt.xticks(xind)
    plt.legend((p1[0], p2[0]), ('Received Friend Request', 'Sent Friend Request'))

    plt.show()

if __name__ == '__main__':
    friends()