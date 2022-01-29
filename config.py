import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    HI = "hi2"

# email server
MAIL_SERVER = '509.hosttech.eu'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = 'gnossomat@z01.ch'
MAIL_PASSWORD = os.environ.get('EMAIL_PWD')

# administrator list
ADMINS = ['christian.ruiz@z01.ch']
