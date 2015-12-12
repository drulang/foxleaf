from __future__ import absolute_import

import mandrill

from bluebutter.celery import app
from cobalt import models

EMAIL_VERIFICATION_URL = "https://www.foxleaf.io/verifyemail?code="
PASSWORD_RESET_VERIFICATION_URL = "https://www.foxleaf.io/changepassword?code="
FROM_EMAIL = "hello@foxleaf.io"

mandrill_client = mandrill.Mandrill('mhXXyzUO9BSq5q2ndstRZQ')


@app.task
def send_user_verification_email(userid):
    # 1. Find user and set new confirmation code
    user = models.User.objects.filter(id=userid).first()
    if not user:
        print("Unable to find user with id: %s" % userid)
    verification_code = models.User.objects.set_user_email_confirmation_code(userid)

    email_url = EMAIL_VERIFICATION_URL + verification_code

    print("User Email Verification URL: %s" % email_url)

    # 2. Send Email
    try:
        message = {
            'from_email': FROM_EMAIL,
            'from_name': 'Hello <Do Not Reply>',
            'headers': {'Reply-To': 'hello@foxleaf.io'},
            'html': '<h1>Welcome to FoxLeaf!</h1><p>Please click the below link to verify your email.</p><p>%s</p>' % email_url,
            'subject': 'FoxLeaf Email Verification',
            'tags': ['email-verification'],
            'text': 'FoxLeaf Email Verification',
            'to': [{'email': user.email,
                    'name': user.username,
                    'type': 'to'}],
        }

        result = mandrill_client.messages.send(message=message, async=False, ip_pool='Main Pool')
    except mandrill.Error as e:
        print('A mandrill error occurred: %s - %s' % (e.__class__, e))
        raise

@app.task
def send_user_password_reset_email(userid):
    # 1. Create verification code
    user = models.User.objects.filter(id=userid).first()
    if not user:
        print("Unable to find user with id: %s" % userid)
    verification_code = models.User.objects.set_user_password_reset_confirmation_code(userid)
    url = PASSWORD_RESET_VERIFICATION_URL + verification_code

    # 2. Send Email
    try:
        message = {
            'from_email': FROM_EMAIL,
            'from_name': 'Hello <Do Not Reply>',
            'html': '<h1>Reset your password!</h1><p>Please click the below link to reset your password.</p><p>%s</p>' % url,
            'subject': 'FoxLeaf password reset',
            'tags': ['password-reset'],
            'text': 'FoxLeaf Password Reset',
            'to': [{'email': user.email,
                    'name': user.username,
                    'type': 'to'}],
        }

        result = mandrill_client.messages.send(message=message, async=False, ip_pool='Main Pool')
    except mandrill.Error as e:
        print('A mandrill error occurred: %s - %s' % (e.__class__, e))
        raise

