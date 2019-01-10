import matplotlib.pyplot as plt
import os
import timestring
import datetime
from datetime import timedelta
import dateutil.parser
import numpy as np
import json
from tabulate import tabulate
from geopy.geocoders import Nominatim
import plotly.plotly as py
import plotly.graph_objs as go

"""
Location history
Author - @animesh-chouhan
"""

today = datetime.datetime.now().strftime('%b %d, %y')
yesterday = (datetime.datetime.now() - timedelta(days=1)).strftime('%b %d, %y')

def diff_location():
    """
        :params none
        Returns the non-repeated address co-ordinates
    """
    loc = raw_input('Enter facebook archive extracted location: ')

    if not os.path.isdir(loc):
        print("The provided location doesn't seem to be right")
        exit(1)
    
    fname = loc+'/location_history/your_location_history.json'
    fname = "your_location_history.json"
    if not os.path.isfile(fname):
        print("The file your_location_history.json is not present at the entered location.")
        exit(1)

    with open(fname, 'r') as f:
        txt = f.read()
    
    raw_data = json.loads(txt)
    usable_data = raw_data["location_history"]
    locations = list()

    for i in usable_data:
        for j in i["attachments"]:
            for k in j["data"]:
                #print(k["place"]["coordinate"]["latitude"], ",", k["place"]["coordinate"]["longitude"], "\n")
                lat  = k["place"]["coordinate"]["latitude"]
                long = k["place"]["coordinate"]["longitude"]
                
                curr_loc = (lat, long)
                locations.append(curr_loc)
    

    diff_loc = list()
    diff_loc.append(locations[0])

    for i in locations[1:]:
        flag = True
        for j in diff_loc:
            threshold = 0.001
            if(abs(j[0]-i[0])<threshold or abs(j[0]-i[0])<threshold):
                flag = False
                break
                
        if flag==True: 
            diff_loc.append(i)
        else :
            pass
    
    return diff_loc       
      

    
def coord2address(locations):    
    """
        :params locations: The locations whose address is to be found
        Prints the address corresponding to the coordinates passed.
    """
    geolocator = Nominatim(user_agent="location-finder" )
    for i in locations:
        coordinate = "{0}, {1}".format(i[0], i[1])
        location = geolocator.reverse(coordinate)
        print(location.address, "\n")
        
       
    
def plot_on_map(locations):    
    """
        :params locations: The locations which have to be plotted
        Plots the point passed
    """    
    mapbox_access_token = 'pk.eyJ1IjoiYW5pbWVzaHNpbmdoIiwiYSI6ImNqcGM1MHpyeDJ0eHgzcXBoZDNrd3dyNnIifQ.N32_UbaPj_KSHkuIJfl33w'

    lat1 = list()
    long1 = list()
    lat_sum = 0
    long_sum = 0

    for i in locations:
        lat1.append(str(i[0]))
        long1.append(str(i[1]))

        lat_sum += i[0]
        long_sum += i[1]

    avg_lat = (lat_sum/len(locations))
    avg_long = (long_sum/len(locations))

    data = [
        go.Scattermapbox(
            lat=lat1,
            lon=long1,
            mode='markers',
            marker=dict(
                size=14
            ),
            text=['Locations'],
        )
    ]

    layout = go.Layout(
        autosize=True,
        hovermode='closest',
        mapbox=dict(
            accesstoken=mapbox_access_token,
            bearing=0,
            center=dict(
                lat=avg_lat,
                lon=avg_long
            ),
            pitch=0,
            zoom=6
        ),
    )

    fig = dict(data=data, layout=layout)
    name = input('Enter your name: ')
    file = 'Location History-' + name
    print("View your plot in your browser at https://plot.ly/~animeshsingh38/ where it is named ",file)
    py.iplot(fig, filename=file)

    
                    
                
    
if __name__ == '__main__':
    
    different_locations = diff_location()
    plot_on_map(different_locations)
