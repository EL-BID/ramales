from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal, QCoreApplication
import requests
import json
import traceback

finished = pyqtSignal(object)
error = pyqtSignal(Exception, basestring)
progress = pyqtSignal(float)
info = pyqtSignal(str)
message = pyqtSignal(str)

translate = QCoreApplication.translate


def is_authorized(user, password):
    return True


def get_surveys(user, password):
    response = {'success': True, 'data': [
        {
            'projectName': 'Colorado',
            'projectId': 1,
            'surveys': [

                {'id': 1, 'name': 'Test'},
                {'id': 2, 'name': 'Test 2'}
            ]

        },
         {
            'projectName': 'Haitien',
            'projectId': 2,
            'surveys': [

                {'id': 1, 'name': 'Test Haitien'},
                {'id': 2, 'name': 'Test Haitien 2'}
            ]

        }
    ]}
    return response


def get_survey_data(survey_id, user, password):
    response = {'success': True, 'data': ['hay data'] }
    return response