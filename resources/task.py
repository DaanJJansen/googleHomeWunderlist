from flask_restful import Resource
from flask import request
from flask_httpauth import HTTPBasicAuth
import configparser
import os

import requests
import json
auth = HTTPBasicAuth()

lstenvvar = ['WUNDERLIST_CLIENT_ID','WUNDERLIST_CLIENT_SECRET','WUNDERLIST_CLIENT_CODE','WUNDERLIST_TASK_AUTH']

config = {}
if (os.environ["USERNAME"] == "RD0003FF61344E$"):
    for envvariable in lstenvvar:
        config[envvariable] = os.environ[envvariable]
else:
    localconfig = configparser.ConfigParser()
    localconfig.read('config/config.ini')
    for envvariable in lstenvvar:
        config[envvariable] = localconfig["DEFAULT"][envvariable]

users = json.loads(config['WUNDERLIST_TASK_AUTH'])

@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None

client_id = config['WUNDERLIST_CLIENT_ID']
token = {'client_id': client_id,
         'client_secret': config['WUNDERLIST_CLIENT_SECRET'],
         'code': config['WUNDERLIST_CLIENT_CODE']
         }
access_token = ""

class task(Resource):
    @auth.login_required    
    def get(self):
        #print(os.environ)
        task.getToken(self)
        parameters = ["Test", "Test2"]
        if type(parameters) is list:
            task.publishTasks(self, parameters)
            strParameters = ",".join(parameters)
            return {"fulfillmentText": "Ok, I'll add " + strParameters + " to grocery list. Anything else?"}
        else:
            return {"fulfillmentText": "Error, input should be list"}
            
        


		
    def post(self):
        task.getToken(self)
        json_data = request.get_json(force=True)
        parameters = json_data['queryResult']['parameters']['tasks']
        
        if type(parameters) is list:
            strParameters = ",".join(parameters)
            task.publishTasks(self, parameters)
            return {"fulfillmentText": "Ok, I'll add " + strParameters + " to grocery list. Anything else?"}
            
        else:
            return {"fulfillmentText": "Error, input should be list"}



    def getToken(self):
        response = requests.post('https://www.wunderlist.com/oauth/access_token',
                                json=token)
        responseJson = response.json()
        access_token = responseJson['access_token']

        self.headers = {"X-Access-Token": access_token,
                        "X-Client-ID": client_id,
                        "Content-Type":"application/json"}


    def publishTasks(self, lstTasks):
        for task in lstTasks:
            payload = {"list_id": 75280967, "title": str(task)}
            response = requests.post('https://a.wunderlist.com/api/v1/tasks',
                                     json=payload,
                                     headers=self.headers)

    def getList(self):
        payload = ""
        response = requests.get('https://a.wunderlist.com/api/v1/lists',
                                data=payload,
                                headers=headers)
    
