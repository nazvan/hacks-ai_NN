import requests
from time import time

ip_address = '25.5.221.55'

data = {
    'robotId':'1',
    'routeId':'fd087117-5a4c-41cb-b367-b4bf7ae55953',
    'latitude':54.1232,
    'longitude':46.3123,
    'timestamp': int(time())
    }
response = requests.post(f'http://{ip_address}:8000/api/add_point', json=data)
print(response.status_code)
print(response.content)