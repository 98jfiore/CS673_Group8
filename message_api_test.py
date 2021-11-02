import os
import tempfile

import pytest 
import json

from message_api import app as api_app

#MOCK OUT cnx.commit()

@pytest.fixture
def client():
  db_fd, db_path = tempfile.mkstemp()
  app = api_app

  with app.test_client() as client:
    with app.app_context():
      #init_db
      print("Test")
    yield client
  
  os.close(db_fd)
  os.unlink(db_path)

def test_get_messages(client):
  rv = client.get('/messages')
  response = json.loads(rv.data.decode("utf-8").replace("'", '"'))
  assert "Missing required parameter" in response['message']['userId']

  rv = client.get('/messages?userId=a')
  response = json.loads(rv.data.decode("utf-8").replace("'", '"'))
  assert "Missing required parameter" in response['message']['contactId']

  rv = client.get('/messages?userId=a&contactId=b')
  response = json.loads(rv.data.decode("utf-8").replace("'", '"'))
  assert "messages" in response.keys()
  assert len(response["messages"]) is 0

  rv = client.get('/messages?userId=aaaa&contactId=bbbb')
  response = json.loads(rv.data.decode("utf-8").replace("'", '"'))
  assert "messages" in response.keys()
  assert len(response["messages"]) is 2
  assert "Hello" in response["messages"][0]["text"]
  assert "Goodbye" in response["messages"][1]["text"]

def test_post_messages(client):
  rv = client.post('/messages')
  response = json.loads(rv.data.decode("utf-8").replace("'", '"'))
  assert "405" in response["message"]["senderId"]
