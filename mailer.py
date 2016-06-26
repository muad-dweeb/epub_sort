#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://developers.google.com/gmail/api/quickstart/python#step_3_set_up_the_sample

from __future__ import print_function
import httplib2
from os import path, makedirs

from apiclient import discovery, errors
from oauth2client import file as oauth2_file
from oauth2client import client, tools

from email.mime.text import MIMEText
from base64 import b64encode

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
SCOPES = 'https://mail.google.com'
CLIENT_SECRET_FILE = 'data/client_secret.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = path.expanduser('~')
    credential_dir = path.join(home_dir, '.credentials')
    if not path.exists(credential_dir):
        makedirs(credential_dir)
    credential_path = path.join(credential_dir,
                                   'gmail-python-quickstart.json')

    store = oauth2_file.Storage(credential_path)
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


def CreateMessage(sender, to, subject, message_text):
  """Create a message for an email.

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

  Returns:
    An object containing a base64 encoded email object.
  """
  message = MIMEText(message_text)
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  return {'raw': b64encode(message.as_string())}


def SendMessage(service, user_id, message):
  """Send an email message.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.

  Returns:
    Sent Message.
  """
  try:
    message = (service.users().messages().send(userId=user_id, body=message)
               .execute())
    print('Message Id: {0:s}'.format(message['id']))
    return message
  except errors.HttpError as error:
      print ('An error occurred: %s' % error)


def main():
    """Shows basic usage of the Gmail API.

    Creates a Gmail API service object and outputs a list of label names
    of the user's Gmail account.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    # test account
    message = CreateMessage('me', 'sirtraline@gmail.com', 'gmail-api test', 'test\n'*10)
    SendMessage(service, 'me', message)

    # List account Labels
    #
    # results = service.users().labels().list(userId='me').execute()
    # labels = results.get('labels', [])
    #
    # if not labels:
    #     print('No labels found.')
    # else:
    #   print('Labels:')
    #   for label in labels:
    #     print(label['name'])


if __name__ == '__main__':
    main()


# def main():
#     parser = argparse.ArgumentParser(description='Send an email')
#     parser.add_argument('credentials', type=str, help='Path to file containing sender\'s account credentials')
#     args = parser.parse_args()
#
#     cred = args.credentials
#     sender_credentials = get_sender_credentials(cred)
#     email = sender_credentials[0].strip()
#     password = sender_credentials[1].strip()
#     establish_connection(email, password)
#
#
# if __name__ == '__main__':
#     main()
