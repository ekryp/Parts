from __future__ import print_function
import time, os, sys
from app.utils.mail import Mail
from app.configs import Configuration
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from apiclient import errors
import base64, mimetypes, os, json, httplib2
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

SmtpHostName = 'smtp.gmail.com'
SmtpPortNumber = '587'

SCOPES = 'https://www.googleapis.com/auth/gmail.compose'
APPLICATION_NAME = 'Gmail API Python Quickstart'

class MailManager(object):
    def __init__(self, **keywords):
        self.from_user = keywords.get('from', 'Arca <noreply@arca.com>')
        self.to = keywords.get('to', '')
        self.subject = keywords.get('subject', '')
        self.cc = keywords.get('cc','')
        self.text = keywords.get('text', '')
        self.html = keywords.get('html', '')
        self.files = keywords.get('files', None)

    def send(self):
        return Mail.send(from_user=self.from_user, to=self.to, cc=self.cc, subject=self.subject, text=self.text, html=self.html, files=self.files)

    def send_report(self, report_name, attachment=1):
        try:
            if not self.subject:
                self.subject = 'New Report Generated:' + report_name
            if not self.text:
                self.text = ('Please find the attached report')
            if(attachment):
                attach_file_path = os.path.join(Configuration.TEMP_FILE_PATH, report_name)
                attach_file = open(attach_file_path, "rb")
                self.files = [('attachment', (report_name, attach_file))]
            return self.send()
        except Exception as e:
            print(str(e))
            print ('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
            return {'error': str(e)}

    def send_mail(self, report_name, attachment=1):
        try:
            if not self.subject:
                self.subject = 'New Report Generated:' + report_name
            if not self.text:
                self.text = ('Please find the attached report')

            msg = MIMEMultipart()
            msg['Subject'] = self.subject
            msg['From'] = self.from_user
            msg['To'] = self.to
            msg['Cc'] = self.cc

            if (attachment):
                attach_file_path = os.path.join(Configuration.TEMP_FILE_PATH, report_name)
                attach_file = open(attach_file_path, "rb")
                self.files = [('attachment', (report_name, attach_file))]
            Mbaseobject = MIMEBase('application', 'octet-stream')
            Mbaseobject.set_payload((attach_file).read())
            encoders.encode_base64(Mbaseobject)
            Mbaseobject.add_header('Content-Disposition', "attachment; filename= %s" % attach_file_path)
            msg.attach(Mbaseobject)
            text = msg.as_string()

            if msg['Cc']:
                Recipients = [msg['To'], msg['Cc']]
            else:
                Recipients = [msg['To']]

            server = smtplib.SMTP(SmtpHostName, SmtpPortNumber)
            server.starttls()
            server.login(self.from_user, 'Cricket@123')
            server.sendmail(msg['From'], [msg['To'],msg['Cc']], text)
            server.close()
        except Exception as e:
            print(str(e))
            print ('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
            return {'error': str(e)}

    def get_credentials(self):
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                   'gmail-python-quickstart.json')

        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else: # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials


    def send_email_google_api(self, report_name, attachment=1):
        message = MIMEMultipart()
        message = MIMEMultipart()
        message['to'] = self.to
        message['from'] = self.from_user
        message['cc'] = self.cc

        if not self.subject:
            self.subject = 'New Report Generated:' + report_name

        message['subject'] = self.subject

        if not self.text:
            self.text = ('Please find the attached report')
            msg = MIMEText(self.text)
            message.attach(msg)

        if (attachment):
            attach_file_path = os.path.join(Configuration.TEMP_FILE_PATH, report_name)
            attach_file = open(attach_file_path, "rb")
            self.files = [('attachment', (report_name, attach_file))]
            msg = MIMEBase('application', 'octet-stream')
            msg.set_payload((attach_file).read())
            attach_file.close()
            msg.add_header('Content-Disposition', "attachment; filename= %s" % attach_file_path)
            message.attach(msg)

        content = {'raw': base64.urlsafe_b64encode(message.as_bytes())}
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('gmail', 'v1', http=http)

        output = content['raw'].decode('utf-8')
        service.users().messages().send(userId=self.from_user, body={'raw':output}).execute()
