import requests

from flask import json

resp = requests.get("http://cs673-group8.herokuapp.com/messages/aaaa/bbbb")
print(resp)
print(resp.json)
print(json.loads(resp.content.decode("utf-8").replace("'", '"')))