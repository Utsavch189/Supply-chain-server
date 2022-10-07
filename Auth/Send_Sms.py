account_sid = 'AC0572e42865afab79a074591312cb5129'
auth_token = '225394e6e9693ced178d9bcb9807617d'

from twilio.rest import Client
client = Client(account_sid, auth_token)

def send(strr,number):
   if(number[0:3]=='+91'):
    client.messages \
        .create(
            body=strr+' '+' is your verification otp',
            from_ =  '+17375307119',
            to =number
        )
   else:
    client.messages \
        .create(
            body=strr+' '+' is your verification otp',
            from_ =  '+17375307119',
            to ='+91'+number
        )