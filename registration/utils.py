
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator    
from django.utils.encoding import force_bytes
from users_auth.tasks import send_mail
from TrackYourAlumni.settings import DEFAULT_FROM_EMAIL


import os
from django.template.loader import render_to_string
def send_invitation(self, request, to_user, subject_content, mail_template):

    users = PasswordResetForm.get_users(self,to_user)
    context={}
    context=send_email(self, users, context, email=to_user)
    email_content = render_to_string(mail_template, context)

    sender =DEFAULT_FROM_EMAIL
    recipient = to_user
    subject = subject_content
    body = email_content

    headers = ["From: " + sender,
                "Subject: " + subject,
                "To: " + recipient,
                "MIME-Version: 1.0",
                "Content-Type: text/html"]
    headers = "\r\n".join(headers)
    send_mail.delay(sender, recipient, headers, body)

def send_email(self, users, context, email=None):
    domain_override = None
    use_https = False
    token_generator = default_token_generator
    email = email if email else self.request.data.get("email")
    if not domain_override:
        current_site = get_current_site(self.request)
        site_name = current_site.name
        domain = current_site.domain
    else:
        site_name = domain = domain_override
    for user in users:
        context.update(
            {
                "email": email,
                "domain": domain,
                "site_name": site_name,
                "uid": urlsafe_base64_encode(force_bytes(user.id)),
                "user": user,
                "token": token_generator.make_token(user),
                "protocol": "https" if use_https else "http",
            }
        )
    return context

