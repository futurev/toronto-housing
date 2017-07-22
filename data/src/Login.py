import requests
from src.private import *
import random
from fake_useragent import UserAgent

class Login:
    """This is the class that handles all operations for logging into mongohouse.com
    """

    def __init__(self):
        return

    def get_session(self):
        self.get_user()
        session = self.init_session()
        session = self.login(session)
        return session

    def get_user(self):
        ua = UserAgent()
        self.user = MONGO_USERS[random.randint(0,len(MONGO_USERS)-1)]

        self.init_headers = {
            'User-Agent': ua[self.user['browser']],
            "Host": "www.mongohouse.com",
            "Proxy-Connection": "keep-alive",
            "Upgrade-Insecure-Requests": 1,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, sdch",
            "Accept-Language": "en-US,en;q=0.8,fr;q=0.6"
            }
        return

    def init_session(self):
        print ('Attempting to get session')
        session = requests.session()
        r = session.get('http://www.mongohouse.com/',headers=self.init_headers)

        cookies = session.cookies.get_dict()
        session_id = cookies['sessionId']
        self.headers = self.init_headers
        self.headers['Origin'] = 'http://www.mongohouse.com'
        self.headers['Referer'] = 'http://www.mongohouse.com/authentication/signin'
        self.headers['Cookie'] = "sessionId=" + session_id
        return session

    def login(self, session):
        r_payload = {'username': self.user['UID'], 'password': self.user['PWD']}
        resp = session.post('http://www.mongohouse.com/api/auth/signin',r_payload,
                            headers=self.headers)
        if resp.status_code == 200:
            print ('Session successfully established')
        else:
            print ('Unable to create session. Session response %s' % resp)
        return session
