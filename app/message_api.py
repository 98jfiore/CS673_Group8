from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
from mock.mock import call
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

passw = os.environ.get("PASSWORD")
user = os.environ.get("USER")
db_host = os.environ.get("DATABASEHOST")
db_name = os.environ.get("DATABASENAME")
cnx = mysql.connector.connect(user=user, password=passw, host=db_host, database=db_name)
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

@app.route('/messages/')
def messages():
  #argument('userId', required=True)
  #argument('contactId', required=True)

  try:
    args = request.get_json()
    resp = {"code": 200, "messages": []}

    # SELECT senderId, receiverId, messageBody, timeSent
    # FROM messages
    # WHERE (senderId=%s AND receiverId=%s) OR (senderId=%s AND receiverId=%s) ORDER BY timeSent""")
    call_query(cursor, get_convo_query, (args['userId'],args['contactId'],args['contactId'],args['userId'],))

    for (senderId, receiverId, messageBody, timeSent) in cursor:
      message = {"text": messageBody,
                  "sender": senderId,
                  "receiver": receiverId,
                  "sendTime": timeSent.strftime("%m/%d/%Y, %H:%M:%S")}
      resp['messages'].append(message)
    
    return jsonify(resp), 200
  except:
    return jsonify({"code": 400}), 400

@app.route('/message/', methods=['POST'])
def post_message():
  #argument('senderId', required=True)
  #argument('receiverId', required=True)
  #argument('messageBody', required=True)

  try:
    args = request.get_json()
    # INSERT INTO messages
    # VALUES (%s, %s, %s, CURRENT_TIMESTAMP, NULL)
    call_query(cursor, add_message, (args['senderId'], args['receiverId'], args['messageBody']))
    cnx.commit()
    return jsonify({"code": 200}), 200
  except:
    return jsonify({"code": 405}), 405

@app.route('/allConversations/')
def allConvos():
  #argument('userId', required=True)

  try:
    args = request.get_json()
    resp = {"code": 200, "conversations": []}
    
    # SELECT DISTINCT receiverId
    # FROM messages
    # WHERE senderId=%s UNION 
    #   SELECT DISTINCT senderId
    #   FROM messages 
    #   WHERE receiverId=%s
    call_query(cursor, get_all_convo_query, 
      (args['userId'],args['userId'],))

    for (contactId) in cursor:
      resp['conversations'].append(contactId[0])
    
    return jsonify(resp), 200
  except:
    return jsonify({"code": 405}), 405

@app.route('/latestMessages')
def latestMessages():
  #argument('userId', required=True)
  #argument('contactId', required=True)

  try:
    args = request.get_json()
    resp = {"code": 200}

    # SELECT senderId, receiverId, messageBody, timeSent
    # FROM messages
    # WHERE (senderId=%s AND receiverId=%s) OR (senderId=%s AND receiverId=%s) 
    # ORDER BY timeSent DESC 
    # LIMIT 1
    call_query(cursor, get_latest_message_query, 
      (args['userId'],args['contactId'],args['contactId'],args['userId'],))

    for (senderId, receiverId, messageBody, timeSent) in cursor:
      resp["text"] = messageBody
      resp["sender"] = senderId,
      resp["receiver"] = receiverId,
      resp["sendTime"] = timeSent.strftime("%m/%d/%Y, %H:%M:%S")

    return jsonify(resp), 200
  except:
    return jsonify({"code": 405}), 405

if __name__ == '__main__':
  app.run()