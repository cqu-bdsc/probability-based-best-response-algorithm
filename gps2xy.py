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

df = pd.read_csv(settings.csv_name)

vehicle_id = df['id'].drop_duplicates()
latitude = df['latitude']
longitude = df['longitude']

# for v_id in vehicle_id:
#     print()

print(latitude.head(3))
print(longitude.head(3))


for lat in latitude:
    for lon in longitude:
        print(lat, lon)
        print(float(lat), float(lon))
        # print(utm.from_latlon(float(lat), lon))