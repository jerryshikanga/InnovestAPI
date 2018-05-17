from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import serializers
from django.template import loader
from django.core.mail import EmailMultiAlternatives
from django.conf import settings


class ReferalSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        """
        Send a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)

        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        if html_email_template_name is not None:
            html_email = loader.render_to_string(html_email_template_name, context)
            email_message.attach_alternative(html_email, 'text/html')

        email_message.send()

    def save(self, request):
        email = self.data['email']
        current_site = get_current_site(request)
        site_name = current_site.name
        domain = current_site.domain
        context = {
            'email': email,
            'domain': domain,
            'site_name': site_name,
            'uid': urlsafe_base64_encode(force_bytes(request.user.pk)).decode(),
            'user': request.user,
            'protocol': 'http',
        }
        self.send_mail( "referrals/referal_subject_template.txt" , "referrals/referal_email.html", context, settings.EMAIL_HOST_USER,
            email, html_email_template_name="referrals/referal_email.html", )
