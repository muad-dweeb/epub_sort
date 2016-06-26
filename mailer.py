#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This code adapted from Gmail API "quickstart":
# https://developers.google.com/gmail/api/quickstart/python#step_3_set_up_the_sample

from __future__ import print_function
from httplib2 import Http
from os import path, makedirs
from email.mime.text import MIMEText
from base64 import b64encode

# GOOGLE
from apiclient import discovery, errors
from oauth2client import file as oauth2_file
from oauth2client import client, tools

# try:
#     import argparse
#     flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
# except ImportError:
#     flags = None
import argparse

# If modifying these scopes, delete your previously saved credentials at ~/.credentials/gmail-python-quickstart.json
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
    credential_path = path.join(credential_dir, 'gmail-python-quickstart.json')
    store = oauth2_file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)

    return credentials


def create_message(sender, to, subject, message_text):
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


def send_message(service, user_id, message):
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
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        print('Message Id: {0:s}'.format(message['id']))
        return message
    except errors.HttpError as error:
        print ('An error occurred: %s' % error)


def list_labels(service, user_id):
    """List account Labels"""

    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    if not labels:
        print('No labels found.')
    else:
      print('Labels:')
      for label in labels:
        print(label['name'])


def main():
    """Sends an email to a recipient.

    Sender account authorization managed through Google API dashboard
    """
    parser = argparse.ArgumentParser(description='Send an email')
    parser.add_argument('-r', '--recipient', type=str, help='destination email address')
    parser.add_argument('-c', '--contents', type=str, help='message body contents')
    args = parser.parse_args()
    recipient = args.recipient
    contents = args.contents

    credentials = get_credentials()
    http = credentials.authorize(Http())
    service = discovery.build('gmail', 'v1', http=http)

    message = create_message('me', recipient, 'gmail-api test', contents)
    send_message(service, 'me', message)


if __name__ == '__main__':
    main()
