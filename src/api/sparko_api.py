import json
import os
import webbrowser

import requests
from datetime import datetime


def find(arr, ele):
    for x in arr:
        if ele(x):
            return x
    return None


class SparkoAPI:

    def __init__(self):
        self.base_url = 'http://192.168.1.33:8080/'

    def fetch_employees(self):
        try:
            res = requests.get(self.base_url + 'members?page=1&limit=10000')
            members = json.loads(res.text)['data']
            result = []
            for member in members:
                res = {
                    'user_id': member['index'],
                    'name': member['user']['firstName'] + ' ' + member['user']['lastName'],
                }
                result.append(res)

            return result

        except Exception as err:
            raise Exception(err)

    def post_attendance(self, data):
        try:

            url = self.base_url + "attendances"
            data["punchTime"] = datetime.strptime(data["punchTime"], "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%dT%H:%M:%SZ")
            payload = json.dumps(data)
            headers = {
                'Content-Type': 'application/json'
            }
            response = requests.request("POST", url, headers=headers, data=payload)

            print(response.text)

            # if response.status_code != 200:
            #     raise Exception(response.text)
        except Exception as err:
            raise Exception(err)
