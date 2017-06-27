import requests
import os
import time
import datetime
import json

class SMZDM:

    site_url = 'https://zhiyou.smzdm.com'
    login_url = site_url + '/user/login/ajax_check'
    checkin_url = site_url + '/user/checkin/jsonp_checkin'

    def __init__(self, username, password):
        self.s = requests.session()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
            'Host': 'zhiyou.smzdm.com',
            'Referer': 'https://zhiyou.smzdm.com/user/login/window/'
            }
        self.s.headers.update(headers)
        self.username = username
        self.password = password

    def signin(self):
        params = {
            'username': self.username,
            'password': self.password
            }
        self.s.post(self.login_url, params)
        r = self.s.get(self.checkin_url)
        code = json.loads(r.text)
        if code['error_code'] == 99:
            return False
        return True

    def autosignin(self):        
        retry = 0
        r = self.signin()        
        while r == False:
            if retry >3:
                break
            time.sleep(60)
            r = self.signin()
            retry +=1

        if retry > 3:
            print('SMZDM sign in failed on {} with account: {}'.format(time.strftime(" %Y/%m/%d %H:%M:%S"), self.username + '\n'))
        else:
            #print(json.loads(r.text))
            print('SMZDM sign in success on {} with account: {}'.format(time.strftime(" %Y/%m/%d %H:%M:%S"), self.username + '\n'))

if __name__ == '__main__':
    username = os.environ.get('SMZDM_USER_NAME').split(',')
    password = os.environ.get('SMZDM_USER_PASSWD').split(',')

    for i in range(len(username)):        
        smzdm = SMZDM(username[i], password[i])
        smzdm.autosignin()

