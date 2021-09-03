from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal, QCoreApplication
import requests
import json
import traceback

finished = pyqtSignal(object)
error = pyqtSignal(Exception, basestring)
progress = pyqtSignal(float)
info = pyqtSignal(str)
message = pyqtSignal(str)
DASHBORAD_URL = "https://dashboard.dev.sanibid.org/"

translate = QCoreApplication.translate


def is_authorized(user, password):
    return True


def get_surveys(user, password):

    url = '{}/api/projects/surveys'.format(DASHBORAD_URL)
    body= {'user': user, 'password': password}
    headers = {'Content-Type': 'application/json'}
    res = dict()
    try:
        r = requests.request("GET", url, headers=headers, data=json.dumps(body))
        res = r.json()
        response = {'success': True, 'data': res['projects']}
    except Exception as e:
        response = {'success': False, 'msg': res['error_message'] if 'error_message' in res else 'Unable to fetch surveys' }
    return response


def get_survey_data(survey_id, user, password):
    url = '{}/api/surveys/{}'.format(DASHBORAD_URL, survey_id)
    body= {'user': user, 'password': password}
    headers = {'Content-Type': 'application/json'}
    res = dict()
    try:
        r = requests.request("GET", url, headers=headers, data=json.dumps(body))        
        res = r.json()
        response = {'success': True, 'data': res['data']}
    except:
        response = {'success': False, 'msg': res['error_message'] if 'error_message' in res else 'Unable to fetch survey data'}
    return response


def send_data(survey_id, user, password, data):
    url = '{}/api/branches'.format(DASHBORAD_URL)
    body = {'user': user, 'password': password, 'data': data, 'survey_id': survey_id}
    headers = {'Content-Type': 'application/json'}
    try:
        r = requests.request("POST", url, headers=headers, data=json.dumps(body))  
        res = r.json()
        if r.status_code == 200:
           return { 'success': True, 'message': res['message']}  
        else:
            return { 'success': False, 'message': res['message']}        
    except:
        response = {'success': False, 'message': 'Unable to publish data'}
    return response