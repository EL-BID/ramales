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


def get_surveys(project_id, user, password):
    response = {'success': True, 'data': []}
    return response
