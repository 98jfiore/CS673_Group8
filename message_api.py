from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast

app = Flask(__name__)
api = Api(app)

class Messages(Resource):
  def get(self):
    parser = reqparse.RequestParser()

    parser.add_argument('userId', required=True)
    parser.add_argument('contactId', required=True)

    args = parser.parse_args()
    return {'text': 'message', 'userId': args['userId'], 'contactId': args['contactId']}
  pass

api.add_resource(Messages, '/messages')

if __name__ == '__main__':
  app.run()