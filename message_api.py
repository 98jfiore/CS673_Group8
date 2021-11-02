from flask import Flask
from flask_restful import Resource, Api, reqparse
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

app = Flask(__name__)
api = Api(app)

class Messages(Resource):
  def get(self):
    parser = reqparse.RequestParser()

    parser.add_argument('userId', required=True)
    parser.add_argument('contactId', required=True)

    args = parser.parse_args()

    resp = {"messages": []}

    cursor.execute(get_convo_query, (args['userId'],args['contactId'],args['contactId'],args['userId'],))
    
    for (senderId, receiverId, messageBody, timeSent) in cursor:
      message = {"text": messageBody,
                  "sender": senderId,
                  "receiver": receiverId,
                  "sendTime": timeSent.strftime("%m/%d/%Y, %H:%M:%S")}
      resp['messages'].append(message)
    
    return resp
  
  def post(self):
    parser = reqparse.RequestParser()

    parser.add_argument('senderId', required=True, help='405')
    parser.add_argument('receiverId', required=True, help='405')
    parser.add_argument('messageBody', required=True, help='405')

    args = parser.parse_args()

    try:
      cursor.execute(add_message, (args['senderId'], args['receiverId'], args['messageBody']))
      cnx.commit()
      return {"code": "200"}
    except:
      return {"code": "405"}
  pass

api.add_resource(Messages, '/messages')

if __name__ == '__main__':
  app.run()