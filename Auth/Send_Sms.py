import vonage

client = vonage.Client(key="ffe48696", secret="VCQX7CJC5haudGbO")
sms = vonage.Sms(client)

def send(strr,number):
   if(number[0:3]=='+91'):
        sms.send_message(
    {
        "from": "U-HUB",
        "to": str(number).replace('+',''),
        "text": strr+' '+' is your verification otp',
    }
)
   else:
        sms.send_message(
    {
        "from": "U-HUB",
        "to": '91'+number,
        "text": strr+' '+' is your verification otp',
    }
)