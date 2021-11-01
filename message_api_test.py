import os
import tempfile

import pytest 
import json

from message_api import app as api_app

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
  assert "message" not in response.keys()