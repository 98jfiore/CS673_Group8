import os
import tempfile

import pytest 
from flask import json

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
    rv = client.get('/messages',
      content_type='application/json', 
      follow_redirects=True)
    response = json.loads(rv.get_data(as_text=True))
    assert 400 == response['code']
    assert 400 == rv.status_code

    rv = client.get('/messages',
      data=json.dumps({'userId': 'aaaa'}),
      content_type='application/json', 
      follow_redirects=True)
    response = json.loads(rv.get_data(as_text=True))
    print(response)
    assert 400 == response['code']
    assert 400 == rv.status_code

  @patch('message_api.call_query', mock_call_query)
  def test_get_messages_no_messages(self, client):
    rv = client.get('/messages',
      data=json.dumps({'userId': 'a', "contactId": 'b'}),
      content_type='application/json', 
      follow_redirects=True)
    response = json.loads(rv.data.decode("utf-8").replace("'", '"'))
    assert "messages" in response.keys()
    assert len(response["messages"]) is 0
    assert 200 == rv.status_code

  @patch('message_api.call_query', mock_call_query)
  def test_get_messages_good_messages(self, client):
    rv = client.get('/messages',
      data=json.dumps({'userId': 'aaaa', "contactId": 'bbbb'}),
      content_type='application/json', 
      follow_redirects=True)
    response = json.loads(rv.data.decode("utf-8").replace("'", '"'))
    assert "messages" in response.keys()
    assert len(response["messages"]) is 3
    assert "Hello" in response["messages"][0]["text"]
    assert "Goodbye" in response["messages"][1]["text"]
    assert "Goodbye Forever" in response["messages"][2]["text"]
    assert 200 == rv.status_code

  @patch('message_api.call_query', mock_call_query)
  @patch('mysql.connector.connection_cext.CMySQLConnection.commit', mock_commit)
  def test_post_messages_bad_input(self, client):
    rv = client.post('/message',
      content_type='application/json', 
      follow_redirects=True)
    response = json.loads(rv.data.decode("utf-8").replace("'", '"'))
    assert 405 == response["code"]
    assert 405 == rv.status_code

    rv = client.post('/message',
      data=json.dumps({'senderId': '1111'}),
      content_type='application/json', 
      follow_redirects=True)
    response = json.loads(rv.data.decode("utf-8").replace("'", '"'))
    assert 405 == response["code"]
    assert 405 == rv.status_code

    rv = client.post('/message',
      data=json.dumps({'senderId': '1111', 'receiverId': '2222'}),
      content_type='application/json', 
      follow_redirects=True)
    response = json.loads(rv.data.decode("utf-8").replace("'", '"'))
    assert 405 == response["code"]
    assert 405 == rv.status_code
  
  @patch('message_api.call_query', mock_call_query)
  @patch('mysql.connector.connection_cext.CMySQLConnection.commit', mock_commit)
  def test_post_messages_good(self, client):
    rv = client.get('/messages',
      data=json.dumps({'userId': '1111', "contactId": '2222'}),
      content_type='application/json', 
      follow_redirects=True)
    response = json.loads(rv.data.decode("utf-8").replace("'", '"'))
    assert "messages" in response.keys()
    assert len(response["messages"]) is 0
  
    rv = client.post('/message',
      data=json.dumps({'senderId': '1111', 'receiverId': '2222', 'messageBody': 'Hi'}),
      content_type='application/json', 
      follow_redirects=True)
    response = json.loads(rv.data.decode("utf-8").replace("'", '"'))
    assert 200 == response["code"]
    assert 200 == rv.status_code

    rv = client.get('/messages',
      data=json.dumps({'userId': '1111', "contactId": '2222'}),
      content_type='application/json', 
      follow_redirects=True)
    response = json.loads(rv.data.decode("utf-8").replace("'", '"'))
    assert "messages" in response.keys()
    assert len(response["messages"]) is 1

  @patch('message_api.call_query', mock_call_query)
  def test_all_conversations_bad(self, client):
    rv = client.get('/allConversations',
      content_type='application/json', 
      follow_redirects=True)
    print(rv.get_data(as_text=True))
    response = json.loads(rv.get_data(as_text=True))
    assert 405 == response["code"]
    assert 405 == rv.status_code
  
  @patch('message_api.call_query', mock_call_query)
  def test_all_conversations_good(self, client):
    rv = client.get('/allConversations',
      data=json.dumps({'userId': 'aaaa'}),
      content_type='application/json', 
      follow_redirects=True)
    response = json.loads(rv.data.decode("utf-8").replace("'", '"'))
    print(response)
    assert "conversations" in response.keys()
    assert len(response["conversations"]) is 2
    assert "bbbb" in response["conversations"]
    assert "cccc" in response["conversations"]
    assert 200 == rv.status_code
  
  @patch('message_api.call_query', mock_call_query)
  def test_latest_messages_bad(self, client):
    rv = client.get('/latestMessages',
      content_type='application/json', 
      follow_redirects=True)
    response = json.loads(rv.data.decode("utf-8").replace("'", '"'))
    assert 405 == response["code"]
    assert 405 == rv.status_code

    rv = client.get('/latestMessages',
      content_type='application/json', 
      data=json.dumps({'userId': 'aaaa'}),
      follow_redirects=True)
    response = json.loads(rv.data.decode("utf-8").replace("'", '"'))
    assert 405 == response["code"]
    assert 405 == rv.status_code
  
  @patch('message_api.call_query', mock_call_query)
  def test_latest_messages_good(self, client):
    rv = client.get('/latestMessages',
      content_type='application/json', 
      data=json.dumps({'userId': 'aaaa', "contactId": 'bbbb'}),
      follow_redirects=True)
    response = json.loads(rv.data.decode("utf-8").replace("'", '"'))
    assert "Goodbye Forever" in response["text"]
    assert 200 == rv.status_code