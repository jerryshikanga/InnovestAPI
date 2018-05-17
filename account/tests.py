from django.test import TestCase
import pympesa
import datetime
import base64
import os


# Create your tests here.
class TestMpesa(TestCase):

    def setUp(self):
        consumer_key = "C9Ne1xW9QOqfXA4pNSqvr30BcPTzSdQm"
        consumer_secret = "h3BvVJk9OBn7YROw"
        environment = "sandbox"
        access_token = pympesa.oauth_generate_token(consumer_key, consumer_secret, grant_type="client_credentials",
                                                    env=environment).json().get("access_token")
        print("Token : " + access_token)
        self.client = pympesa.Pympesa(access_token, env=environment)
        self.online_short_code = "174379"
        self.online_pass_key = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
        self.validation_url = "http://shikanga.pythonanaywhere.com/account/api/"
        self.confirmation_url = "http://shikanga.pythonanaywhere.com/account/api/"
        self.short_code_1 = "600348"
        self.short_code_2 = "6000"
        self.initiator_name_sc_1 = "apitest361"
        self.security_credential_sc_1 = "361reset"
        self.test_msisdn = "254708374149"
        self.initiator_security_credential = \
            os.getenv("TEST_MPESA_INITIATOR_SECURITY_CREDENTIAL")

    def test_lipa_na_mpesa_online_payment(self):
        timenow = datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d%H%M%S")
        data = self.online_short_code + \
               self.online_pass_key + \
               timenow
        data_bytes = data.encode("utf-8")
        password_bytes = base64.b64encode(data_bytes)
        password = password_bytes.decode("utf-8")
        resp = self.client.lipa_na_mpesa_online_payment(
            BusinessShortCode=self.online_short_code,
            Password= password,
            Timestamp=timenow,
            TransactionType="CustomerPayBillOnline",
            Amount=12,
            PartyA="254727447101",
            PartyB= self.online_short_code,
            PhoneNumber="254727447101",
            CallBackURL=self.confirmation_url,
            AccountReference="pympesa-dev-test",
            TransactionDesc="pympesa-dev-test"
        )
        print("Response body : "+resp.content.decode("utf-8"))
        self.assertEqual(resp.status_code, 200)
        result = resp.json()
        self.assertIn("ResponseCode", result)

    def test_b2c_payment_request(self):
        resp = self.client.b2c_payment_request(
            InitiatorName=self.initiator_name_sc_1,
            SecurityCredential=self.security_credential_sc_1,
            CommandID="BusinessPayment",
            Amount=50,
            PartyA=self.short_code_1,
            PartyB=self.test_msisdn,
            Remarks="Testing B2C",
            QueueTimeOutURL=self.validation_url,
            ResultURL=self.validation_url,
            Occassion="Testcases"
        )
        print(resp.content)
        self.assertEqual(resp.status_code, 200)