from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
from mock.mock import call
import mysql.connector
import os
from dotenv import load_dotenv
from werkzeug.wrappers import response

load_dotenv()

passw = os.environ.get("PASSWORD")
user = os.environ.get("USER")
db_host = os.environ.get("DATABASEHOST")
db_name = os.environ.get("DATABASENAME")

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

@app.route('/messages/<userId>/<contactId>')
def messages(userId, contactId):
  cnx = mysql.connector.connect(user=user, password=passw, host=db_host, database=db_name)
  cursor = cnx.cursor()
  
  #argument('userId', required=True)
  #argument('contactId', required=True)

  try:
    args = request.view_args
    resp = {"code": 200, "messages": []}
    print("data is " + format(args))
    # SELECT senderId, receiverId, messageBody, timeSent
    # FROM messages
    # WHERE (senderId=%s AND receiverId=%s) OR (senderId=%s AND receiverId=%s) ORDER BY timeSent""")
    print("HERE")
    call_query(cursor, get_convo_query, (args['userId'],args['contactId'],args['contactId'],args['userId'],))
    print("HERE")
    for (senderId, receiverId, messageBody, timeSent) in cursor:
      message = {"text": messageBody,
                  "sender": senderId,
                  "receiver": receiverId,
                  "createdAt": timeSent.strftime("%m/%d/%Y, %H:%M:%S"),
                  "user":{"_id":userId}
                  }
      resp['messages'].append(message)
    
    response = jsonify(resp)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response, 200
  except Exception as e:
    print(e)
    response = jsonify({"code": 400})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response, 400

@app.route('/message/<senderId>/<receiverId>/<messageBody>', methods=['POST'])
def post_message(senderId, receiverId, messageBody):
  cnx = mysql.connector.connect(user=user, password=passw, host=db_host, database=db_name)
  cursor = cnx.cursor()
  #argument('senderId', required=True)
  #argument('receiverId', required=True)
  #argument('messageBody', required=True)

  try:
    args = request.view_args
    # INSERT INTO messages
    # VALUES (%s, %s, %s, CURRENT_TIMESTAMP, NULL)
    call_query(cursor, add_message, (args['senderId'], args['receiverId'], args['messageBody']))
    cnx.commit()
    response = jsonify({"code": 200})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response, 200
  except Exception as e:
    print(e)
    response = jsonify({"code": 405})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response, 405

@app.route('/allConversations/<userId>')
def allConvos(userId):
  cnx = mysql.connector.connect(user=user, password=passw, host=db_host, database=db_name)
  cursor = cnx.cursor()
  #argument('userId', required=True)

  try:
    args = request.view_args
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
      resp['conversations'].append({"id": contactId[0]})
    
    response = jsonify(resp)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response, 200
  except Exception as e:
    print(e)
    response = jsonify({"code": 405})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response, 405

@app.route('/latestMessages/<userId>/<contactId>')
def latestMessages(userId, contactId):
  cnx = mysql.connector.connect(user=user, password=passw, host=db_host, database=db_name)
  cursor = cnx.cursor()
  #argument('userId', required=True)
  #argument('contactId', required=True)

  try:
    args = request.view_args
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
      resp["createdAt"] = timeSent.strftime("%m/%d/%Y, %H:%M:%S")

    response = jsonify(resp)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response, 200
  except Exception as e:
    print(e)
    response = jsonify({"code": 405})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response, 405

if __name__ == '__main__':
  app.run()