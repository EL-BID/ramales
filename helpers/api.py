from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal, QCoreApplication
import requests
import json
import traceback

finished = pyqtSignal(object)
error = pyqtSignal(Exception, basestring)
progress = pyqtSignal(float)
info = pyqtSignal(str)
message = pyqtSignal(str)
DASHBORAD_URL = "http://localhost:3000"

translate = QCoreApplication.translate


def is_authorized(user, password):
    return True


def get_surveys(user, password):

    url = '{}/api/projects/surveys?user={}'.format(DASHBORAD_URL, user)
    headers = {'Content-Type': 'application/json'}
    try:
        r = requests.request("GET", url, headers=headers, data={})
        res = r.json()
        response = {'success': True, 'data': res['projects']}
    except:
        response = {'success': False, 'msg': 'unable to fetch surveys'}
    return response


def get_survey_data(survey_id, user, password):
    url = '{}/api/surveys/{}'.format(DASHBORAD_URL, survey_id)
    headers = {'Content-Type': 'application/json'}
    try:
        r = requests.request("GET", url, headers=headers, data={})
        res = r.json()
        response = {'success': True, 'data': res['data']}
    except:
        response = {'success': False, 'msg': 'unable to fetch survey data'}
    return response