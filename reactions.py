import json
import os
import matplotlib.pyplot as plt
import numpy as np
import re
import datetime as dt
from datetime import timedelta
import timestring

def reactions():
    loc = input('Enter facebook archive extracted location: ')
    if not os.path.isdir(loc):
        print("The provided location doesn't seem to be right")
        exit(1)
    
    fname = loc+'/likes_and_reactions/posts_and_comments.json'
    if not os.path.isfile(fname):
        print("The file posts_and_commments.json is not present at the entered location.")
        exit(1)

    with open(fname) as f:
        base_data = json.load(f)
    
    data = base_data['reactions']
    reactions = []
    count = []

    # Counting the occurence of each reaction
    
    for ele in data:
        reaction = ele['data'][0]['reaction']['reaction']
        reactions.append(reaction)

    count.append(reactions.count("LIKE"))
    count.append(reactions.count("HAHA"))
    count.append(reactions.count("WOW"))
    count.append(reactions.count("LOVE"))
    count.append(reactions.count("ANGER"))
    count.append(reactions.count("SORRY"))
    
    # Plotting the counts
    
    x = np.array([0,1,2,3,4,5])
    y = np.array(count)
    x_ticks = ['LIKE', 'HAHA', 'WOW', 'LOVE', 'ANGER', 'SORRY']
    plt.xticks(x,x_ticks)
    plt.plot(x,y,linestyle='--',marker='o')
    plt.ylabel('Frequency')
    plt.show()
    
    # Top10 friends whom you are most likely to react to
    
    pattern1 = r"(?:likes ).+\b"
    pattern2 = r"(?:to ).+\b"
    names = []
    for ele in data:
        title = ele["title"]
        first_names = re.findall(pattern1, title)
        if len(first_names)>0:
            if len(first_names[0].split())>1:
                names.append(first_names[0].split()[1] + " " + first_names[0].split()[2])
        else:
            first_names = re.findall(pattern2, title)
            if len(first_names)>0:
                if len(first_names[0].split())>1:
                    names.append(first_names[0].split()[1] + " " + first_names[0].split()[2])

    name_counter = {}
    for name in names:
        if name in name_counter:
            name_counter[name]+=1
        else:
            name_counter[name]=1
    popular_names = sorted(name_counter,key = name_counter.get, reverse = True)
    top_10 = popular_names[:10]
    for friend in top_10:
        friend = re.sub('\'s', '', friend)
        print(friend)
    
    # Month Wise Distribution of Reactions
    
    count_month = [0]*12
    for ele in data:
        timestamp = ele['timestamp']
        month = dt.datetime.fromtimestamp(timestamp).month
        count_month[month-1]+=1
    plt.plot(count_month,linestyle="--", marker="^", color="g")
    plt.ylabel("Frequency")
    plt.xlabel("Month Number")
    plt.show()
    
    # Line plot for each reaction
    
    rxnList = ['LIKE', 'HAHA', 'WOW', 'LOVE', 'ANGER', 'SORRY']
    for rxn in rxnList:
        dataTemp = [item for item in data if item["data"][0]["reaction"]["reaction"]==rxn]
        dates = [timestring.Date(i["timestamp"]).date for i in dataTemp]
        dates.reverse()

        firstdate = dates[0]    
        maxdays = int((dates[-1] - firstdate).total_seconds() / 86400) + 1
        reactionCount = [0]*int(maxdays)

        for i in range(len(dates)):
            days_diff = (dates[i] - firstdate).total_seconds() / 86400
            reactionCount[int(days_diff)] += 1

        xaxis = [ dt.datetime.now() - timedelta(days=maxdays-i) for i in range(maxdays) ]
        cumulative_reactions = np.cumsum(reactionCount).tolist()

        plt.plot(xaxis,cumulative_reactions,linewidth=3.0, label=rxn)
    plt.legend(loc='upper left')
    plt.title("Reactions on posts", fontsize=16, fontweight='bold')
    plt.xlabel("Time")
    plt.ylabel("Cumulative Sum of Reactions")
    plt.show()
    
if __name__ == '__main__':
    reactions()