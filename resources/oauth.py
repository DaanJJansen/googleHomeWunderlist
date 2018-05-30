from flask_restful import Resource
from flask import request
from flask_httpauth import HTTPBasicAuth
import requests
import json

auth = HTTPBasicAuth()



class oauth(Resource):
    @auth.login_required
    def get(self):
        json_data = request.get_json(force=True)
        data = json_data['queryResult']['action']
        return {"fulfillmentText": json_data}
		
    def post(self):
        json_data = request.get_json(force=True)
        data = json_data['queryResult']['action']
        return {"fulfillmentText": json_data}

