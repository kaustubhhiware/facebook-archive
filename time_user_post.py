import os
import numpy as np
import matplotlib.pylab as plt
import json
from datetime import datetime, timedelta
import  json
import argparse
import warnings
import sys
import pandas as pd

warnings.filterwarnings('ignore')


def user_post(loc):
    if loc =="":
        loc = input("Enter facebook archive extracted location: ")
    if not os.path.isdir(loc):
        print("The provided location doesn't seem to right")
        exit(1)

    posts = loc+"/posts/your_posts.json"

    if not os.path.isfile(posts):
        print("The file posts is not present in the entered loation")
        exit(1)

    with open(posts, 'r') as f:
        file = f.read()

    data = json.loads(file)


    lis = list()
    for i in data["status_updates"]:
        print(i)
        dates = pd.to_datetime(datetime.fromtimestamp(i["timestamp"]).strftime("%Y/%m/%d %H:%M:%S"))
        hour = dates.strftime("%H")
        lis.append(int(hour))

    count_post = {}
    for i in lis:
        try:
            count_post[i] = count_post[i]+1
        except Exception as e:
            count_post[i] = 0
            count_post[i] = count_post[i]+1

    count_post = sorted(count_post.items())

    x, y = zip(*count_post)

    print("plotting number of post with respect to hours in which user like to post")
    f, ax = plt.subplots()
    ax2 = ax.twinx()
    ax.plot(x, y, label = "post so far in hour")
    ax.set_ylabel("number of post")
    ax.set_xlabel("hours")
    plt.show()






if __name__ == '__main__':

    loc = ""
    if len(sys.argv) > 1:
        loc = sys.argv[1]
    user_post(loc)








