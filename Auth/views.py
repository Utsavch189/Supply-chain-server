from rest_framework.response import Response
from rest_framework.decorators import api_view
from .Jwt import auths,Refresh_Token
from .models import *
import json
from datetime import date
from .UID import creates
import random
from .Mail import otp_mail,passwordUpdate_mail,middle_otp_mail
from Admins.models import ApprovedUsers
from .Enc_Dec import encryption,decryption
from .Send_Sms import send
from django.contrib.auth.hashers import make_password,check_password


@api_view(['POST','GET'])
def login(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    email=body['uid']
    password=(body['password'])
    if ApprovedUsers.objects.exists():
        obj=ApprovedUsers.objects.filter(email=email)
        passwords=obj.values('password')[0]['password']
        if not passwords:
            return Response({"status":253,"msg":"Password expired. Create a new one"})
        else:
            if check_password(password,passwords):
                data={
                    "uid":obj.values('email')[0]['email'],
                    "password":(obj.values('password')[0]['password']),
                    "name":obj.values('name')[0]['name'],
                    "id":obj.values('id_no')[0]['id_no'],
                    "role":obj.values('role')[0]['role'],
                    "phone":obj.values('phone')[0]['phone'],
                    "account_creates":obj.values('approved_at')[0]['approved_at'].strftime('%m/%d/%Y')
                }
                a=auths(data,"")
                JWTs=a.encoded_jwt()
                return Response({"token":JWTs,"status":200})
            else:
                return Response({"msg":"Invalid Credentials","status":400})
    else:
        return Response({"msg":"Invalid Credentials","status":400})


@api_view(['POST'])
def createuser(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    name=body['fname']+body['lname']
    number=body['number']
    email=body['email']
    whatsapp_no=body['whatsapp']
    gender=body['gender']
    role=body['role']
    password=body['password']
    obb=ApprovedUsers.objects.filter(email=email)
    obj=Register.objects.filter(email=email)

    if (obb.exists()) or (obj.exists()):
        return Response({"msg":"Email Already Exists","status":400})
    
    else:  
        try:
            idd=creates()
            x=Register(name=name,phone=number,email=email,password=make_password(password),gender=gender,whatsapp_no=whatsapp_no,role=role,id_no=idd,created_at=date.today())
            x.save()
            return Response({"msg":"Successfully Registered","status":200})
        except:
            return Response({"msg":"Something Wrong","status":400})


@api_view(['POST'])
def sendotp(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    email=body['email']
    typed=body['type']
    obb=ApprovedUsers.objects.filter(email=email)
    if obb.exists():
        name=obb.values('name')[0]['name']
        otp=random.randint(1111,9999)
        try:
            otpobj=OTP.objects.filter(target=email).filter(typed='authenticated').filter(blocked=False)
            if otpobj.exists():
                created_date=otpobj.values('created_at_date')[0]['created_at_date'].strftime('%m/%d/%Y')
                if(date.today().strftime('%m/%d/%Y')==created_date):
                     time_created_minute=otpobj.values('created_at_time')[0]['created_at_time'].strftime("%M")
                     time_created_hour=otpobj.values('created_at_time')[0]['created_at_time'].strftime("%H")
                     if datetime.now().time().strftime("%H")==time_created_hour and int(datetime.now().time().strftime("%M"))-int(time_created_minute)==5:                     
                        return Response({"msg":"valid","status":200})
                     else:
                        otpobj.delete()
                        x=OTP(target=email,otp=otp,typed=typed,tried=0,blocked=False,created_at_date=date.today(),created_at_time=datetime.now().time())
                        x.save()
                        otp_mail(email,name,otp)
                        return Response({"msg":"successful","status":200})
                else:
                    otpobj.delete()
                    x=OTP(target=email,otp=otp,typed=typed,tried=0,blocked=False,created_at_date=date.today(),created_at_time=datetime.now().time())
                    x.save()
                    otp_mail(email,name,otp)
                    return Response({"msg":"successful","status":200})
                
            else:
                x=OTP(target=email,otp=otp,typed=typed,tried=0,blocked=False,created_at_date=date.today(),created_at_time=datetime.now().time())
                x.save()
                otp_mail(email,name,otp)
                return Response({"msg":"successful","status":200})
        except:
            return Response({"msg":"error","status":400})


@api_view(['POST'])
def resetpassword(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    email=body['email']
    password=body['password']
    f=body['f']
    s=body['s']
    t=body['t']
    fo=body['fo']
    usersotp=int(str(f)+str(s)+str(t)+str(fo))
    obb=ApprovedUsers.objects.filter(email=email)
    if obb.exists():
        name=obb.values('name')[0]['name']
        otpobj=OTP.objects.filter(target=email).filter(typed='authenticated').filter(blocked=False)
        otp=int(otpobj.values('otp')[0]['otp'])
        
        if usersotp==otp:
            try:
                obb.update(password=make_password(password))
                passwordUpdate_mail(email,name)
                otpobj.delete()
                return Response({"msg":"Password Changed","status":200})
            except:
                return Response({"msg":"error","status":400})
        else:
            tried=otpobj.values('tried')[0]['tried']
            if tried<2:
                otps=random.randint(1111,9999)
                otpobj.update(otp=otps)
                otpobj.update(tried=int(tried)+1)
                otpobj.update(created_at_time=datetime.now().time())
                otp_mail(email,name,otps)
                return Response({"msg":f"not matching {3-otpobj.values('tried')[0]['tried']} tries left","status":400})
            else:
                otpobj.update(blocked=True)
                return Response({"msg":"max trying limit exceed","status":400})
    return Response({"msg":"email or phone otp doesn't exists","status":400})





@api_view(['POST'])
def sendotp_middlereg(request):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        email=body['email']
        phone=body['phone']
        typed=body['type']

        eotp=random.randint(1111,9999)
        potp=random.randint(1111,9999)
        try:
            obj1=OTP.objects.filter(target=email).filter(typed='not-authenticated').filter(blocked=False)
            obj2=OTP.objects.filter(target=phone).filter(typed='not-authenticated').filter(blocked=False)

            if obj1.exists() and obj2.exists():
                obj1.delete()
                obj2.delete()
                x=OTP(target=email,otp=eotp,typed=typed,tried=0,blocked=False,created_at_date=date.today(),created_at_time=datetime.now().time())
                x.save()
                y=OTP(target=phone,otp=potp,typed=typed,tried=0,blocked=False,created_at_date=date.today(),created_at_time=datetime.now().time())
                y.save()
                middle_otp_mail(email,eotp)
                send(str(potp),str(phone))
                return Response({"msg":"successful","status":200})
            else:
                x=OTP(target=email,otp=eotp,typed=typed,tried=0,blocked=False,created_at_date=date.today(),created_at_time=datetime.now().time())
                x.save()
                y=OTP(target=phone,otp=potp,typed=typed,tried=0,blocked=False,created_at_date=date.today(),created_at_time=datetime.now().time())
                y.save()
                middle_otp_mail(email,eotp)
                send(str(potp),str(phone))
                return Response({"msg":"successful","status":200})
        except:
            return Response({"msg":"error","status":400})


@api_view(['POST'])
def verify_middlereg(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    email=body['email']
    phone=body['phone']

    ef=body['ef']
    es=body['es']
    et=body['et']
    efo=body['efo']

    pf=body['pf']
    ps=body['ps']
    pt=body['pt']
    pfo=body['pfo']

    email_otp=str(str(ef)+str(es)+str(et)+str(efo))
    phone_otp=str(str(pf)+str(ps)+str(pt)+str(pfo))

    obj1=OTP.objects.filter(target=email).filter(typed='not-authenticated').filter(blocked=False)
    obj2=OTP.objects.filter(target=phone).filter(typed='not-authenticated').filter(blocked=False)

    if obj1.exists() and obj2.exists():
        if email_otp==obj1.values('otp')[0]['otp'] and phone_otp==obj2.values('otp')[0]['otp']:
            obj1.delete()
            obj2.delete()
            return Response({"msg":"successful","status":200})
        else:
                tried_email=obj1.values('tried')[0]['tried']
                tried_phone=obj2.values('tried')[0]['tried']
                if tried_email<2 and tried_phone<2:
                    eotp=random.randint(1111,9999)
                    potp=random.randint(1111,9999)

                    obj1.update(otp=eotp)
                    obj1.update(tried=int(tried_email)+1)
                    obj1.update(created_at_time=datetime.now().time())

                    obj2.update(otp=potp)
                    obj2.update(tried=int(tried_phone)+1)
                    obj2.update(created_at_time=datetime.now().time())

                    middle_otp_mail(email,eotp)
                    send(str(potp),str(phone))

                    return Response({"msg":f"not matching {3-obj1.values('tried')[0]['tried']} tries left","status":400})
                else:
                    obj1.update(blocked=True)
                    obj2.update(blocked=True)
                    return Response({"msg":"max trying limit exceed","status":400})
            

    return Response({"msg":"email or phone otp doesn't exists","status":400})



@api_view(['POST'])
def refresh_token(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    tokens=body['token']

    token=Refresh_Token(tokens)
    if token=='delete':
        return Response({"msg":"delete","status":200})
    else:
        if token:
            return Response({"token":token,"status":200})
        else:
            return Response({"msg":"not expired yet!","status":400})


@api_view(['POST'])
def is_block(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    email=body['email']
    phone=body['phone']

    if email and phone:
        obj=OTP.objects.filter(target=email).filter(typed='not-authenticated').filter(blocked=True)
        obj1=OTP.objects.filter(target=phone).filter(typed='not-authenticated').filter(blocked=True)
        if obj.exists() and obj1.exists():
            created_date=obj.values('created_at_date')[0]['created_at_date'].strftime('%m/%d/%Y')
            if(date.today().strftime('%m/%d/%Y')==created_date):
                time_created_minute=obj.values('created_at_time')[0]['created_at_time'].strftime("%M")
                time_created_hour=obj.values('created_at_time')[0]['created_at_time'].strftime("%H")
                if datetime.now().time().strftime("%H")==time_created_hour and int(datetime.now().time().strftime("%M"))-int(time_created_minute)>=30:
                    obj.delete()
                    obj1.delete()
                    return Response({"status":200})
                else:
                    return Response({"status":400,"time-left":30-(int(datetime.now().time().strftime("%M"))-int(time_created_minute))})
            else:
                obj.delete()
                obj1.delete()
                return Response({"status":200})
        else:
            return Response({"status":200})
    elif email and (not phone):
        obj=OTP.objects.filter(target=email).filter(typed='authenticated').filter(blocked=True)
       
        if obj.exists():
            created_date=obj.values('created_at_date')[0]['created_at_date'].strftime('%m/%d/%Y')
            if(date.today().strftime('%m/%d/%Y')==created_date):
                time_created_minute=obj.values('created_at_time')[0]['created_at_time'].strftime("%M")
                time_created_hour=obj.values('created_at_time')[0]['created_at_time'].strftime("%H")
                if datetime.now().time().strftime("%H")==time_created_hour and int(datetime.now().time().strftime("%M"))-int(time_created_minute)>=30:
                    obj.delete()
                    obj1.delete()
                    return Response({"status":200})
                else:
                    return Response({"status":400,"time-left":30-(int(datetime.now().time().strftime("%M"))-int(time_created_minute))})
            else:
                obj.delete()
                obj1.delete()
                return Response({"status":200})
        else:
            return Response({"status":200})
    else:
        return Response({"msg":"running"})




