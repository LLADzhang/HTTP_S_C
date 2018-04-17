import requests
import numpy as np
import http.client
import json
from time import sleep

arr = np.zeros((224,224,3)).tolist()
js=json.dumps(arr)
connection = http.client.HTTPConnection('128.46.73.217:8000')

headers = {'Content-type': 'application/json'}

foo = {'pic': js}
json_foo = json.dumps(foo)
while(1):
    connection.request('POST', '/', json_foo, headers)

    response = connection.getresponse()
    print(json.loads(response.read().decode())['reply'])
    sleep(1)
