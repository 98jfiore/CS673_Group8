from flask import Flask
from flask_restful import Resource, Api, reqparse
from mock.mock import call
import pandas as pd
import ast
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

passw = os.environ.get("PASSWORD")
user = os.environ.get("USER")
cnx = mysql.connector.connect(user=user, password=passw, host='127.0.0.1', database='sys')
cursor = cnx.cursor()

get_convo_query = ("""SELECT senderId, receiverId, messageBody, timeSent
        FROM messages
        WHERE (senderId=%s AND receiverId=%s) OR (senderId=%s AND receiverId=%s) ORDER BY timeSent""")

add_message = ("""INSERT INTO messages
              VALUES (%s, %s, %s, CURRENT_TIMESTAMP, NULL)""")

get_all_convo_query = ("""SELECT DISTINCT receiverId
              FROM messages
              WHERE senderId=%s UNION SELECT DISTINCT senderId FROM messages WHERE receiverId=%s""")

get_latest_message_query = ("""SELECT senderId, receiverId, messageBody, timeSent
        FROM messages
        WHERE (senderId=%s AND receiverId=%s) OR (senderId=%s AND receiverId=%s) ORDER BY timeSent DESC LIMIT 1""")

app = Flask(__name__)
api = Api(app)

#Here for the express purpose of making tests easier
def call_query(curs, query, spec):
  curs.execute(query, spec)

class Messages(Resource):
  def get(self):
    parser = reqparse.RequestParser()

    parser.add_argument('userId', required=True)
    parser.add_argument('contactId', required=True)
    
    args = parser.parse_args()
    
    try:
      resp = {"code": 200, "messages": []}

      #cursor.execute(get_convo_query, (args['userId'],args['contactId'],args['contactId'],args['userId'],))
      call_query(cursor, get_convo_query, (args['userId'],args['contactId'],args['contactId'],args['userId'],))

      for (senderId, receiverId, messageBody, timeSent) in cursor:
        message = {"text": messageBody,
                    "sender": senderId,
                    "receiver": receiverId,
                    "sendTime": timeSent.strftime("%m/%d/%Y, %H:%M:%S")}
        resp['messages'].append(message)
      
      return resp
    except:
      return {"code": "400"}

  
  def post(self):
    parser = reqparse.RequestParser()

    parser.add_argument('senderId', required=True, help='405')
    parser.add_argument('receiverId', required=True, help='405')
    parser.add_argument('messageBody', required=True, help='405')

    args = parser.parse_args()

    try:
      call_query(cursor, add_message, (args['senderId'], args['receiverId'], args['messageBody']))
      cnx.commit()
      return {"code": "200"}
    except:
      return {"code": "405"}
  pass

class Conversations(Resource):
  def get(self):
    parser = reqparse.RequestParser()

    parser.add_argument('userId', required=True)
    
    args = parser.parse_args()

    try:
      resp = {"code": 200, "conversations": []}
      call_query(cursor, get_all_convo_query, 
        (args['userId'],args['userId'],))

      for (contactId) in cursor:
        resp['conversations'].append(contactId[0])
      
      return resp
    except:
      return {"code": "400"}
  pass

class LatestMessages(Resource):
  def get(self):
    parser = reqparse.RequestParser()

    parser.add_argument('userId', required=True)
    parser.add_argument('contactId', required=True)
    
    args = parser.parse_args()

    try:
      resp = {"code": 200}
      call_query(cursor, get_latest_message_query, 
        (args['userId'],args['contactId'],args['contactId'],args['userId'],))

      for (senderId, receiverId, messageBody, timeSent) in cursor:
        resp["text"] = messageBody
        resp["sender"] = senderId,
        resp["receiver"] = receiverId,
        resp["sendTime"] = timeSent.strftime("%m/%d/%Y, %H:%M:%S")

      return resp
    except:
      return {"code": "400"}
  pass


api.add_resource(Messages, '/messages')
api.add_resource(Conversations, '/allConversations')
api.add_resource(LatestMessages, '/latestMessages')

if __name__ == '__main__':
  app.run()