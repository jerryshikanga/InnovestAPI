from rest_framework import serializers
from .models import Account
from django.contrib.auth.models import User
from django.template import loader
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
import re

UserModel = get_user_model()


class AccountSerializer(serializers.ModelSerializer):
    interests = serializers.StringRelatedField(many=True)
    user = serializers.StringRelatedField()

    class Meta:
        model = Account
        fields = ['user', 'interests', 'balance', 'picture', 'telephone']
        read_only_fields = ['user', 'balance',]


class AccountUpdateSerializer(serializers.Serializer) :
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    picture = serializers.ImageField(required=False)
    telephone = serializers.IntegerField(required=False)
    username = serializers.CharField(required=False)

    def create(self, validated_data):
        user = User.objects.get(username=validated_data['username'])
        account = user.account
        user.first_name = validated_data.get("first_name")
        user.last_name = validated_data.get("last_name")
        account.picture = validated_data.get("picture")
        account.telephone = validated_data.get("telephone")
        user.save()
        account.save()
        return  account

    def validate(self, attrs):
        telephone = attrs.get("telephone")
        if not re.match("254*", str(telephone)):
            serializers.ValidationError()
            raise serializers.ValidationError("Telephone must begin with +254")
        return attrs


class UserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'username', 'password1', 'password2', 'is_staff')
        read_only_fields = ('is_staff', 'is_superuser', 'is_active', 'date_joined', 'id')
        write_only_fields = ('password1', 'password2')

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'],
                                        validated_data['password1'])
        user.first_name = validated_data['first_name']
        user.last_name = validated_data['last_name']
        user.save()
        return user

    def validate(self, data):
        if not data.get('password1') or not data.get('password1'):
            raise serializers.ValidationError("Please enter a password and "
                                              "confirm it.")

        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError("Those passwords don't match.")

        return data


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class PasswordResetSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

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

    def get_users(self, email):
        """Given an email, return matching user(s) who should receive a reset.

        This allows subclasses to more easily customize the default policies
        that prevent inactive users and users with unusable passwords from
        resetting their password.
        """
        active_users = UserModel._default_manager.filter(**{
            '%s__iexact' % UserModel.get_email_field_name(): email,
            'is_active': True,
        })
        return (u for u in active_users if u.has_usable_password())

    def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None, html_email_template_name=None,
             extra_email_context=None):
        """
        Generate a one-use only link for resetting password and send it to the
        user.
        """
        email = self.data["email"]
        for user in self.get_users(email):
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override
            context = {
                'email': email,
                'domain': domain,
                'site_name': site_name,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': 'https' if use_https else 'http',
            }
            if extra_email_context is not None:
                context.update(extra_email_context)
            self.send_mail(
                subject_template_name, email_template_name, context, from_email,
                email, html_email_template_name=html_email_template_name,
            )


class MpesaC2BValidationSerializer(serializers.Serializer):
    """ expected payload // Validation Response
     {
    "TransactionType":"",
    "TransID":"LGR219G3EY",
    "TransTime":"20170727104247",
    "TransAmount":"10.00",
    "BusinessShortCode":"600134",
    "BillRefNumber":"xyz",
    "InvoiceNumber":"",
    "OrgAccountBalance":"",
    "ThirdPartyTransID":"",
    "MSISDN":"254708374149",
    "FirstName":"John",
    "MiddleName":"Doe",
    "LastName":""
    } """

    TransactionType = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    TransID = serializers.CharField()
    TransTime = serializers.CharField()
    TransAmount = serializers.FloatField()
    BusinessShortCode = serializers.CharField()
    BillRefNumber = serializers.CharField()
    InvoiceNumber = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    OrgAccountBalance = serializers.FloatField()
    ThirdPartyTransID = serializers.CharField()
    MSISDN = serializers.CharField()
    FirstName = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    MiddleName = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    LastName = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class MpesaC2bConfirmationSerializer(serializers.Serializer):
    """//Expected Confirmation Respose
    {
    "TransactionType":"",
    "TransID":"LGR219G3EY",
    "TransTime":"20170727104247",
    "TransAmount":"10.00",
    "BusinessShortCode":"600134",
    "BillRefNumber":"xyz",
    "InvoiceNumber":"",
    "OrgAccountBalance":"49197.00",
    "ThirdPartyTransID":"1234567890",
    "MSISDN":"254708374149",
    "FirstName":"John",
    "MiddleName":"",
    "LastName":""
    }"""

    TransactionType = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    TransID = serializers.CharField()
    TransTime = serializers.CharField()
    TransAmount = serializers.FloatField()
    BusinessShortCode = serializers.CharField()
    BillRefNumber = serializers.CharField()
    InvoiceNumber = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    OrgAccountBalance = serializers.FloatField()
    ThirdPartyTransID = serializers.CharField()
    MSISDN = serializers.CharField()
    FirstName = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    MiddleName = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    LastName = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        user = User.objects.get(username=validated_data['BillRefNumber'])
        account = Account.objects.get(user=user)
        account.deposit(validated_data['TransAmount'])
        account.save()
        return True


class MpesaB2CListnerSerializer(serializers.Serializer):
    TransAmount = serializers.FloatField()
    BillRefNumber = serializers.CharField()

    def create(self, validated_data):
        user = User.objects.get(username=validated_data['BillRefNumber'])
        account = Account.objects.get(user=user)
        account.withdraw(validated_data['TransAmount'])
        account.save()
        return True


class WithdrawRequestSerializer(serializers.Serializer):
    """docstring for WithdrawDepositResquestSerializer."""
    amount = serializers.IntegerField(required=True)


class DepositRequestSerializer(serializers.Serializer):
    """docstring for WithdrawDepositResquestSerializer."""
    amount = serializers.IntegerField(required=True)
