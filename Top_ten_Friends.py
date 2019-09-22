
# coding: utf-8

# In[4]:


import pandas as pd
import numpy as np
import json 
import os
import datetime
import matplotlib.pyplot as plt
import argparse 
import operator
import re


class dd_list(dict):
    def __missing__(self,k):
        r = self[k] = []
        return r


class FriendsIMessage(dd_list):
    
    def __init__(self,name,num_friends):
        self.name=name
        self.num_friends=num_friends
        self.conversations=[]
        self.who_i_message_counts=dict()
        self.who_i_message=dd_list()
        self.who_message_me_counts=dict()
        self.who_message_me=dd_list()
        self.top_ten=dd_list()
        self.top_ten_counts=dict()
        self.top_ten_i=dd_list()
        self.top_ten_i_counts=dict()
        self.daily_aggregate=dd_list()
        self.daily_aggregate_i=dd_list()
        self.message_filename = "message.json"
        
    def __call__(self,messages_dir):
        self.conversations=self.get_all_conversations(messages_dir)
        self.populate_all_messages(messages_dir)
        self.create_manipulate_dataframes_plot()
        self.visualize_data(self.daily_aggregate,"day","cumulative_daily_messages","top_ten_friends_who_i_message")
        self.dataframe_show(self.top_ten_counts,"NO._OF_MESSAGES_SENT")
        self.visualize_data(self.daily_aggregate_i,"day","cumulative_daily_messages","top_ten_friends_who_message_me")
        self.dataframe_show(self.top_ten_i_counts,"NO._OF_MESSAGES_RECEIVED")
        
    def get_all_conversations(self,messages_dir):
        """
            :params message_dir: The location of the directory
            :returns: a list of all the directory i.e conversations
            Returns a list of all the converstaion that has taken place.
        """
        conversations=[]
        dirs=[convo for convo in os.listdir(messages_dir) if os.path.isdir(messages_dir+"/"+convo)==True]
        for d in dirs:
            files=[x for x in os.listdir(messages_dir+"/"+d) if os.path.isfile(messages_dir+"/"+d+"/"+x)==True]
            try:
                if re.search(r'message(_\d+)?\.json', files[0]):
                    self.message_filename = files[0]
                    conversations.append(d)
            except:
                pass
        return conversations
            
            
    def populate_all_messages(self,messages_dir):
        """
           This method finds the top ten friends whom i message and stores their 
           messages friendwise.
        """
        for convo in self.conversations:
            f=messages_dir+"/"+convo+"/"+self.message_filename
            with open(f) as msg_json_f:
                msg_json=json.load(msg_json_f)
                count=0
                count_i=0
                #checks for a friend and not a group
                if len(msg_json["participants"])==2:
                    for msg in msg_json["messages"]:
                        values=[]
                        values=[x for x in msg.values()]
                        if values[0]==self.name:#count has the total no. of messages i have messaged to a particular friend
                            count=count+1 
                            for x in msg_json["participants"]:
                                title=[y for y in x.values()]
                                self.who_i_message[title[0]].append(msg)
                                
                        else:#count_i has the total no. of messages who had messaged me
                            count_i=count_i+1
                            for x in msg_json["participants"]:
                                title_i=[y for y in x.values()]
                                self.who_message_me[title_i[0]].append(msg)
                                
                        
                                    
                                    
                    for x in msg_json["participants"]:
                        title1=[y for y in x.values()]
                        self.who_i_message_counts[title1[0]]=count
                        self.who_message_me_counts[title1[0]]=count_i
        
                                
                                    
        
        sv=sorted(self.who_i_message_counts.items(),key=operator.itemgetter(1),reverse=True)#finds the top ten friends
        sv_i=sorted(self.who_message_me_counts.items(),key=operator.itemgetter(1),reverse=True)
        flag=0
        flag_i=0
        for x,y in sv:
            
            if flag==self.num_friends:
                break
            else:
                self.top_ten[x]=self.who_i_message[x]
                self.top_ten_counts[x]=y
            flag=flag+1       
        for x,y in sv_i:
            
            if flag_i==self.num_friends:
                break
            else:
                self.top_ten_i[x]=self.who_message_me[x]
                self.top_ten_i_counts[x]=y
            flag_i=flag_i+1
       
                

                
                
            
        
    def create_manipulate_dataframes_plot(self):
        """
            This method is used to get all the required columns
            to the dataframe and store the appropriate aggregation in the
            variables and plot each friends messages as a function of time(days) 
        """
        for x in self.top_ten.keys():
            
            msgdf = pd.DataFrame.from_dict(self.top_ten[x])
            msgdf = msgdf[["timestamp_ms", "sender_name"]]
            msgdf["time"] = msgdf["timestamp_ms"].apply(
            lambda x: datetime.datetime.fromtimestamp(x/1000))
            msgdf["day"] = msgdf["time"].apply(lambda convo: convo.day)
            
            self.daily_aggregate[x].append(msgdf["day"].value_counts())
            
        for x in self.top_ten_i.keys():
            
            msgdf_i = pd.DataFrame.from_dict(self.top_ten_i[x])
            msgdf_i = msgdf_i[["timestamp_ms", "sender_name"]]
            msgdf_i["time"] = msgdf_i["timestamp_ms"].apply(
            lambda x: datetime.datetime.fromtimestamp(x/1000))
            msgdf_i["day"] = msgdf_i["time"].apply(lambda convo: convo.day)
            
            self.daily_aggregate_i[x].append(msgdf_i["day"].value_counts())
            
            
    def dataframe_show(self,tabular,address):
        '''
           shows the dataframe containing no. of messages per friend
        '''
        keys=[x for x in tabular.keys()]
        values=[x for x in tabular.values()]
        df=pd.DataFrame({'NAME':keys,address:values})
        print(df)


   
    def cumulative_list(self, lists):
        """
            :params list: The list of values that has to be cummilated
            :returns: The cummilated list

            Turn the dicrete values into continuous value
        """
        cu_list = []
        length = len(lists)
        cu_list = [sum(lists[0:convo + 1]) for convo in range(0, length)]
        return cu_list
   
    
    def visualize_data(self,visualize_points,xlable,ylable,title):
        """
            Create visualization for the given points and show the lables
        """
        stacklist_x=[]
        stacklist_y=[]
        stacklist_labels=[]
        for a in visualize_points.keys():
            
            
            x_axis = visualize_points[a][0].index.tolist()[::-1]
            y_axis = visualize_points[a][0].tolist()[::-1]
            y_axis = self.cumulative_list(y_axis)
            x, y = zip(*sorted(zip(x_axis, y_axis), key=operator.itemgetter(0)))
            stacklist_x.append(x)
            stacklist_y.append(y)
            stacklist_labels.append(a)
       
        
        fig=plt.figure(figsize=(20,10))
        ax=fig.add_subplot(111)
        for x in range(0,self.num_friends):
            ax.plot(stacklist_x[x],stacklist_y[x],zorder=1,label=stacklist_labels[x])
            ax.scatter(stacklist_x[x],stacklist_y[x],zorder=2)
        plt.legend(loc="upper left")
        plt.xlabel(xlable)
        plt.ylabel(ylable)
        plt.title(title)
        plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--msg', help="Message directory location")
    parser.add_argument('--name',help="your facebook name")
    parser.add_argument('--num_friends',help="no. of friends you want to plot")
    args = parser.parse_args()
    if args.name is None:
        name=input('enter your official facebook name: ')
    else:
        name=args.name
    if args.num_friends is None:
        num_friends=10
    else:
        num_friends=int(args.num_friends)
    if args.msg is None:
        loc = input('Enter facebook archive extracted location: ')
        #currently only focused on inbox
        loc = loc + "/messages/inbox"
    else:
        loc = args.msg
    if not os.path.isdir(loc):
        print("The provided location doesn't seem to be right")
        exit(1)
    top_10_friends = FriendsIMessage(name,num_friends)
    top_10_friends(loc)

       
        
        
                                    
        


# In[ ]:




