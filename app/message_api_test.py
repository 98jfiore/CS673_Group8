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
    app.config['DEBUG'] = True
    app.config['TESTING'] = True
    
    with app.test_client() as client:
      with app.app_context():
        #init_db
        print("Test")
      
      yield client
    
    os.close(db_fd)
    os.unlink(db_path)

  @patch('message_api.call_query', mock_call_query)
  def test_get_messages_bad_input(self, client):
    rv = client.get('/messages/',
      content_type='application/json', 
      follow_redirects=True)
    assert 404 == rv.status_code

    rv = client.get('/messages/aaaa/',
      content_type='application/json', 
      follow_redirects=True)
    assert 404 == rv.status_code

  @patch('message_api.call_query', mock_call_query)
  def test_get_messages_no_messages(self, client):
    rv = client.get('/messages/a/b',
      content_type='application/json', 
      follow_redirects=True)
    response = json.loads(rv.data.decode("utf-8").replace("'", '"'))
    assert "messages" in response.keys()
    assert len(response["messages"]) is 0
    assert 200 == rv.status_code

  @patch('message_api.call_query', mock_call_query)
  def test_get_messages_good_messages(self, client):
    rv = client.get('/messages/aaaa/bbbb',
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
    assert 404 == rv.status_code

    rv = client.post('/message/1111',
      content_type='application/json', 
      follow_redirects=True)
    assert 404 == rv.status_code

    rv = client.post('/message/1111/2222/',
      content_type='application/json', 
      follow_redirects=True)
    assert 404 == rv.status_code
    
  @patch('message_api.call_query', mock_call_query)
  @patch('mysql.connector.connection_cext.CMySQLConnection.commit', mock_commit)
  def test_post_messages_good(self, client):
    rv = client.get('/messages/1111/2222',
      content_type='application/json', 
      follow_redirects=True)
    response = json.loads(rv.data.decode("utf-8").replace("'", '"'))
    assert "messages" in response.keys()
    assert len(response["messages"]) is 0
  
    rv = client.post('/message/1111/2222/Hi',
      content_type='application/json', 
      follow_redirects=True)
    response = json.loads(rv.data.decode("utf-8").replace("'", '"'))
    assert 200 == response["code"]
    assert 200 == rv.status_code
    
  @patch('message_api.call_query', mock_call_query)
  def test_all_conversations_bad(self, client):
    rv = client.get('/allConversations',
      content_type='application/json', 
      follow_redirects=True)
    print(rv.get_data(as_text=True))
    assert 404 == rv.status_code
  
  @patch('message_api.call_query', mock_call_query)
  def test_all_conversations_good(self, client):
    rv = client.get('/allConversations/aaaa',
      content_type='application/json', 
      follow_redirects=True)
    response = json.loads(rv.data.decode("utf-8").replace("'", '"'))
    print(response)
    assert "conversations" in response.keys()
    assert len(response["conversations"]) is 2
    assert {"id": "bbbb"} in response["conversations"]
    assert {"id": "cccc"} in response["conversations"]
    assert 200 == rv.status_code
  
  @patch('message_api.call_query', mock_call_query)
  def test_all_conversations_none(self, client):
    rv = client.get('/allConversations/zzzz',
      content_type='application/json', 
      follow_redirects=True)
    response = json.loads(rv.data.decode("utf-8").replace("'", '"'))
    print(response)
    assert "conversations" in response.keys()
    assert len(response["conversations"]) is 0
    assert 200 == rv.status_code
  
  @patch('message_api.call_query', mock_call_query)
  def test_latest_messages_bad(self, client):
    rv = client.get('/latestMessages',
      content_type='application/json', 
      follow_redirects=True)
    assert 404 == rv.status_code

    rv = client.get('/latestMessages/aaaa',
      content_type='application/json', 
      follow_redirects=True)
    assert 404 == rv.status_code
  
  @patch('message_api.call_query', mock_call_query)
  def test_latest_messages_good(self, client):
    rv = client.get('/latestMessages/aaaa/bbbb',
      content_type='application/json', 
      follow_redirects=True)
    response = json.loads(rv.data.decode("utf-8").replace("'", '"'))
    assert "Goodbye Forever" in response["text"]
    assert 200 == rv.status_code
  
  @patch('message_api.call_query', mock_call_query)
  def test_latest_messages_none(self, client):
    rv = client.get('/latestMessages/zzzz/xxxx',
      content_type='application/json', 
      follow_redirects=True)
    response = json.loads(rv.data.decode("utf-8").replace("'", '"'))
    print(response)
    assert "" in response["text"]
    assert 200 == rv.status_code