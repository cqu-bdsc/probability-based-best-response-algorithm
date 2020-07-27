"""
author: neardws
data: 16/7/2020

The objection is to obtain the converted UTM coordinates from WGS84 coordinates

utm usage
utm.from_latlon(latitude, longitude)
"""
import pandas as pd
import utm
from config import settings


def renew_csv():
    df = pd.read_csv(settings.csv_name)
    vehicle_id = df['id']
    time = df['time']
    latitude = df['latitude']
    longitude = df['longitude']
    print("read csv success")
    list_xy = list_latlon_to_xy(latitude, longitude)
    if list_xy:
        list_x = list_xy[0]
        list_y = list_xy[1]
        new_df = pd.DataFrame({'id': vehicle_id, 'time': time, 'x': list_x, 'y': list_y})
        new_df.to_csv(settings.xy_csv_name, index=False)


def list_latlon_to_xy(list_latitude, list_longitude):
    list_x = []
    list_y = []
    if len(list_latitude) == len(list_longitude):
        length = len(list_latitude)
        for i in range(length):
            xy_coordinate = utm.from_latlon(list_latitude[i], list_longitude[i])
            list_x.append(float(xy_coordinate[0]))
            list_y.append(float(xy_coordinate[1]))
            print(i)
    if len(list_x) == len(list_y):
        return list_x, list_y
    else:
        return None


if __name__ == '__main__':
    renew_csv()
