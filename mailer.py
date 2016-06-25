#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Tutorial referenced = https://automatetheboringstuff.com/chapter16/

import smtplib


smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
# Entering type(smtpObj) shows you that there’s an SMTP object stored in smtpObj.
# You’ll need this SMTP object in order to call the methods that log you in and send emails.
# If the smptlib.SMTP() call is not successful, your SMTP server might not support TLS on port 587.
# In this case, you will need to create an SMTP object using smtplib.SMTP_SSL() and port 465 instead.

if smtpObj.ehlo()[0] == 250:
    print("Handshake successful")
else:
    print("Handshake failed")
    exit()

if smtpObj.starttls()[0] == 220:
    print("Server is ready for TLS Encryption")
else:
    print("WARNING:\tEncryption unverified")

