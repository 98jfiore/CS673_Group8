import os
import tempfile

import pytest 
import json

from mock import patch, Mock

from message_api import app as api_app
from message_api import call_query

def mock_call_query(curs, query, specification):
  query = query.replace("messages", "test_messages")
  return curs.execute(query, specification)

def mock_commit(self):
  return True

#MOCK OUT cnx.commit()
class TestMessages:
  @pytest.fixture
  def client(self):
    db_fd, db_path = tempfile.mkstemp()
    app = api_app

    with app.test_client() as client:
      with app.app_context():
        #init_db
        print("Test")
      yield client
    
    os.close(db_fd)
    os.unlink(db_path)

  @patch('message_api.call_query', mock_call_query)
  def test_get_messages_bad_input(self, client):
    rv = client.get('/messages')
    response = json.loads(rv.data.decode("utf-8").replace("'", '"'))
    assert "Missing required parameter" in response['message']['userId']

    rv = client.get('/messages?userId=a')
    response = json.loads(rv.data.decode("utf-8").replace("'", '"'))
    assert "Missing required parameter" in response['message']['contactId']

  @patch('message_api.call_query', mock_call_query)
  def test_get_messages_no_messages(self, client):
    rv = client.get('/messages?userId=a&contactId=b')
    response = json.loads(rv.data.decode("utf-8").replace("'", '"'))
    assert "messages" in response.keys()
    assert len(response["messages"]) is 0

  @patch('message_api.call_query', mock_call_query)
  def test_get_messages_good_messages(self, client):
    rv = client.get('/messages?userId=aaaa&contactId=bbbb')
    response = json.loads(rv.data.decode("utf-8").replace("'", '"'))
    assert "messages" in response.keys()
    assert len(response["messages"]) is 3
    assert "Hello" in response["messages"][0]["text"]
    assert "Goodbye" in response["messages"][1]["text"]
    assert "Goodbye Forever" in response["messages"][2]["text"]


  @patch('message_api.call_query', mock_call_query)
  @patch('mysql.connector.connection_cext.CMySQLConnection.commit', mock_commit)
  def test_post_messages_bad_input(self, client):
    rv = client.post('/messages')
    response = json.loads(rv.data.decode("utf-8").replace("'", '"'))
    assert "405" in response["message"]["senderId"]

    rv = client.post('/messages?senderId=1111')
    response = json.loads(rv.data.decode("utf-8").replace("'", '"'))
    assert "405" in response["message"]["receiverId"]

    rv = client.post('/messages?senderId=1111&receiverId=2222')
    response = json.loads(rv.data.decode("utf-8").replace("'", '"'))
    assert "405" in response["message"]["messageBody"]
  
  @patch('message_api.call_query', mock_call_query)
  @patch('mysql.connector.connection_cext.CMySQLConnection.commit', mock_commit)
  def test_post_messages_good(self, client):
    rv = client.get('/messages?userId=1111&contactId=2222')
    response = json.loads(rv.data.decode("utf-8").replace("'", '"'))
    assert "messages" in response.keys()
    assert len(response["messages"]) is 0
  
    rv = client.post('/messages?senderId=1111&receiverId=2222&messageBody=Hi')
    response = json.loads(rv.data.decode("utf-8").replace("'", '"'))
    assert "200" in response["code"]

    rv = client.get('/messages?userId=1111&contactId=2222')
    response = json.loads(rv.data.decode("utf-8").replace("'", '"'))
    assert "messages" in response.keys()
    assert len(response["messages"]) is 1
  
  @patch('message_api.call_query', mock_call_query)
  def test_all_conversations_bad(self, client):
    rv = client.get('/allConversations')
    response = json.loads(rv.data.decode("utf-8").replace("'", '"'))
    assert "Missing" in response["message"]["userId"]
  
  @patch('message_api.call_query', mock_call_query)
  def test_all_conversations_good(self, client):
    rv = client.get('/allConversations?userId=aaaa')
    response = json.loads(rv.data.decode("utf-8").replace("'", '"'))
    assert "conversations" in response.keys()
    assert len(response["conversations"]) is 2
    assert "bbbb" in response["conversations"]
    assert "cccc" in response["conversations"]