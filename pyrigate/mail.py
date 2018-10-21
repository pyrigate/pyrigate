# -*- coding: utf-8 -*-

"""Functions for sending emails."""

from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
import mimetypes
import os
import smtplib

from pyrigate.logging import error, output
from pyrigate.settings import get_settings


def encode_attachment(attachment, ctype):
    """Encode and return an attachment as a MIME type."""
    maintype, subtype = ctype.split('/', 1)

    if maintype == 'text':
        mode, cons = '', MIMEText
    elif maintype == 'image':
        mode, cons = 'rb', MIMEImage
    else:
        error(ValueError, "Unsupported attachment type '{0}'"
              .format(maintype))

    with open(attachment, mode=mode) as fh:
        attachment = cons(fh.read(), _subtype=subtype)
        attachment.add_header('Content-Disposition', 'attachment',
                              filename=attachment)

    return attachment


def get_password():
    """Get and return the mail password from the environment."""
    password = os.environ.get('PYRIGATE_MAIL_PASSWORD', None)

    if not password:
        output('Cannot send mail, PYRIGATE_MAIL_PASSWORD not set')

    return password


def send_mail(subject, sender, receivers, message, attachments=None,
              server=None, port=None):
    """Send an email, possibly with attachments.

    If server or port are not specified, uses the values from the
    user_settings.py file.

    The password is set through the PYRIGATE_MAIL_PASSWORD environment
    variable.

    """
    if attachments:
        mime = MIMEMultipart()

        for attachment in attachments:
            ctype, encoding = mimetypes.guess_type(attachment)

            if ctype is None or encoding is not None:
                error(ValueError, "Failed to guess mimetype of '{0}'"
                      .format(attachment))

            mime.attach(encode_attachment(attachment, ctype))

        mime.attach(MIMEText(message))
    else:
        mime = MIMEText(message)

    mime['Subject'] = subject
    mime['From'] = sender
    mime['To'] = COMMASPACE.join(receivers)
    mime['Date'] = formatdate(localtime=True)

    smtp = None
    settings = get_settings()
    server = server if server else settings['email']['server']
    port = port if port else settings['email']['port']

    try:
        if settings['email']['use_ssl']:
            smtp = smtplib.SMTP_SSL(server, port)
        else:
            smtp = smtplib.SMTP(server, port)
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()

        password = get_password()

        if password:
            smtp.login(sender, password)
            smtp.sendmail(sender, receivers, message)
    finally:
        if smtp:
            smtp.close()
