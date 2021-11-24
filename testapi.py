import requests

from flask import json

resp = requests.get(" http://127.0.0.1:5000/messages/aaaa/bbbb")
print(resp)
print(resp.json)
print(json.loads(resp.content.decode("utf-8").replace("'", '"')))