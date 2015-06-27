import smtplib
import email.utils
from email.mime.text import MIMEText

from mailconfig import *


class R3Mail():

    def send(self, subject, text, to_emails, from_name='r3bot', from_email='r3bot-no-reply@chaos-at-home.org'):
        msg = MIMEText(text)
        msg.set_unixfrom('author')
        #msg['To'] = email.utils.formataddr(('Recipient', to_emails))
        msg['From'] = email.utils.formataddr((from_name, from_email))
        msg['Subject'] = subject

        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        try:
            # server.set_debuglevel(True)

            # identify ourselves, prompting server for supported features
            server.ehlo()

            # check for STARTTLS
            if server.has_extn('STARTTLS'):
                print "## STARTTLS! :)"
                server.starttls()
                server.ehlo()  # re-identify ourselves over TLS connection
            else:
                print "## no STARTTLS!? fail."
                exit()

            # print "logging in with", SMTP_USER, ':', SMTP_PASSWORD

            # Pretend the SMTP server supports some forms of authentication.
            server.esmtp_features['auth'] = 'PLAIN'

            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(from_email, to_emails, msg.as_string())
        finally:
            server.quit()
