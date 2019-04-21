# Version - 1.1
# Date - 2019/01/27
# Author - Sam

from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from configparser import ConfigParser
import requests
import hashlib
from urllib.parse import unquote

# Init flask framework
app = Flask(__name__)
api = Api(app)

# Init api parameter
alert = {}

# parser api post parameter
parser = reqparse.RequestParser()
parser.add_argument('msg_id')
parser.add_argument('task_id')
parser.add_argument('task_type')
parser.add_argument('fault_time')
parser.add_argument('message_type')
parser.add_argument('message_status')
parser.add_argument('task_summary')
parser.add_argument('content')
parser.add_argument('token')
parser.add_argument('message_detail')


class GetVersion:
    @staticmethod
    def show():
        msg = "Guardain-bao Version:1.1 \n"
        print(msg)
        return


class GetConfig:
    def __init__(self, configfile):
        self.config = ConfigParser()
        self.config.read(configfile)

    # Get Team+ config
    def get_teamplus_api_url(self):
        api_url = self.config.get('TeamPlus', 'api_url')
        return api_url

    def get_teamplus_api_config(self):
        account = self.config.get('TeamPlus', 'account')
        api_key = self.config.get('TeamPlus', 'api_key')
        chat_sn = self.config.get('TeamPlus', 'chat_sn')
        teamplus_config = {'account': account, 'api_key': api_key, 'chat_sn': chat_sn, 'Content_type': '1', 'msg_content': ''}
        return teamplus_config

    # Get Jiankongbao config
    def get_jiankongbao_token(self):
        api_token = self.config.get('JiankongbaoAlert', 'api_token')
        return api_token

    # Get this service port
    def get_api_port(self):
        api_port = self.config.get('JiankongbaoAlert', 'api_port')
        return api_port

    # Get prefix in config file
    def get_prefix(self):
        prefix = self.config.get('JiankongbaoAlert', 'prefix')
        return prefix


# Send message to team+ API
class TeamplusApi:
    def __init__(self, api_url, config):
        self.config = config
        self.api_url = api_url

    def send_message(self, msg):
        self.config['msg_content'] = msg
        return requests.post(self.api_url, self.config).text


# Convert to MD5 hash
class MD5Convert:
    @staticmethod
    def convert(data):
        m = hashlib.md5()
        m.update(data.encode("utf-8"))
        h = m.hexdigest()
        return h


# Main class for this API Service
class JiankongbaoAlert(Resource):
    def __init__(self):
        # TeamPlus API url & API_KEY
        self.teamplus_url = config.get_teamplus_api_url()
        self.teamplus_config = config.get_teamplus_api_config()
        self.teamplus = TeamplusApi(self.teamplus_url, self.teamplus_config)
        # Jiankongbao API_KEY
        self.api_token = config.get_jiankongbao_token()
        # Get the prefix need to show when alerting in team+
        self.prefix = config.get_prefix()

    def get(self):
        return

    def post(self):
        # Get post parameter
        args = parser.parse_args()
        alert['alert'] = {'msg_id': args['msg_id'],
                          'task_id': args['task_id'],
                          'task_type': args['task_type'],
                          'fault_time': args['fault_time'],
                          'message_type': args['message_type'],
                          'message_status': args['message_status'],
                          'task_summary': args['task_summary'],
                          'content': args['content'],
                          'message_detail': args['message_detail'],
                          'token': args['token']}
        # Check this post is legal by MD5Check
        md5test = alert['alert']['msg_id']+alert['alert']['task_id']+alert['alert']['fault_time']+self.api_token
        if MD5Convert.convert(md5test) == alert['alert']['token']:
            # Send message to team+ by urldecode content
            msg = alert['alert']['task_summary']+" - "+unquote(alert['alert']['content'])
            self.teamplus.send_message(self.prefix+msg)
            # self.teamplus.send_message(alert['alert'].values())
            return alert['alert'], 201
        return


# API URL = http://{IP}:{Port}/post
api.add_resource(JiankongbaoAlert, '/post')

if __name__ == '__main__':
    GetVersion.show()
    config = GetConfig("guardian.conf")
    web_port = config.get_api_port()

    app.run(
        host='0.0.0.0',
        port=web_port,
        debug=True
    )
