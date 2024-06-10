import os
import clicksend_client
from clicksend_client.rest import ApiException
from dotenv import load_dotenv
from django.conf import settings

BASE_DIR = settings.BASE_DIR
env_path = load_dotenv(os.path.join(BASE_DIR, '.env'))
load_dotenv(env_path)

configuration = clicksend_client.Configuration()
configuration.username = 'eugeneemma7@gmail.com'
configuration.password = '0021FD10-8C13-BE5A-6D07-CBB382FCFFEB'

# creating api instance
api_instance = clicksend_client.SMSApi(clicksend_client.ApiClient(configuration))


def send_otp(phone_number, otp):

    # sms instance
    sms_message = clicksend_client.SmsMessage(
        body=f'Here is your otp {otp}',
        to=phone_number,
        source='python'
    )

    sms_messages = clicksend_client.SmsMessageCollection(messages=[sms_message])
    try:
        api_response = api_instance.sms_send_post(sms_messages)
        return api_response
    except Exception as e:
        print(str(e))
        return None
