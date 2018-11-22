import requests

from app.configs import Configuration

class Mail(object):
    _send_mail_api = Configuration.MAIL_GUN_API_URL + 'messages'

    @classmethod
    def send(cls, from_user=None, to=None, cc=None, subject='', text='', html='', files=None):
        #@TODO: Send an email asynchronously
        to = to if type(to) == list else [to] if type(to) in [str] else None
        payload = {
                    'from': from_user,
                    'to': to,
                    'subject': subject,
                    'text': text,
                    'html': html
                }
        if cc:
            payload['cc'] = cc
        try:
            print(requests.post(
                cls._send_mail_api,
                auth=('api', Configuration.MAIL_GUN_API_KEY),
                files=files,
                data=payload))
            return True
        except Exception as e:
            print(str(e))
            print ('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
            return False