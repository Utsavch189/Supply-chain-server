account_sid = 'ACf966c417a8f93c74f0b9bcbcb1c29206'
auth_token = 'fc4543970aa5931656d90ede7d40c3c5'

from twilio.rest import Client
client = Client(account_sid, auth_token)

def send(strr,number):
   if(number[0:3]=='+91'):
    client.messages \
        .create(
            body=strr+' '+' is your verification otp',
            from_ =  '+19259403550',
            to =number
        )
   else:
    client.messages \
        .create(
            body=strr+' '+' is your verification otp',
            from_ =  '+19259403550',
            to ='+91'+number
        )