import requests
from time import time, sleep
import json

ip_address = '25.5.221.55'

(lat_1, lon_1), (lat_2, lon_2) = (37.5831,55.7446),(37.5942,55.7351)
response = requests.get(f'https://routing.openstreetmap.de/routed-car/route/v1/driving/{lat_1},{lon_1};{lat_2},{lon_2}?geometries=polyline&steps=true')
routes = json.loads(response.content.decode('utf-8'))['routes'][0]['legs'][0]['steps']
for point in routes:
    lat, lon = point['maneuver']['location']
    data = {
        'robotId':'1',
        'latitude':lat,
        'longitude':lon,
        'timestamp': int(time())
        }
    response = requests.post(f'http://{ip_address}:8000/api/add_point', json=data)
    sleep(1)