# -*- coding: utf-8 -*-

"""Functions for sending emails."""

import pyrigate
import mimetypes
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def encode_attachement(attachment, ctype):
    """Encode and return an attachment as a MIME type."""
    maintype, subtype = ctype.split('/', 1)

    if maintype == 'text':
        with open(attachment) as fh:
            attachment = MIMEText(fh.read(), _subtype=subtype)
    elif maintype == 'image':
        with open(attachment, 'rb') as fh:
            attachment = MIMEImage(fh.read(), _subtype=subtype)
    else:
        pyrigate.error(ValueError, '')

    attachment.add_header('Content-Disposition', 'attachment',
                          filename=attachment)
    return attachment


def send_mail(subject, sender, receivers, message, attachments=[],
              server=None, port=None):
    """Send an email, possibly with attachments.

    If server or port are not specified, use the values from the settings file.

    """
    mime = MIMEText(message) if not attachments else MIMEMultipart()
    mime['Subject'] = subject
    mime['From'] = sender
    mime['To'] = ', '.join(receivers)

    for attachment in attachments:
        filename, _ = attachment
        ctype, encoding = mimetypes.guess_type(filename)

        if ctype is None or encoding is not None:
            pyrigate.error(ValueError, "")

        mime.attach(encode_attachement(attachment, ctype))

    smtp = None
    server = pyrigate.settings['email']['server'] if server is None else server
    port = pyrigate.settings['email']['port'] if port is None else port

    try:
        smtp = smtplib.SMTP(server, port)
        # smtp.starttls()
        smtp.sendmail(sender, receivers, mime.as_string())
    finally:
        if smtp:
            smtp.quit()
