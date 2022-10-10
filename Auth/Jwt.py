import jwt
from datetime import datetime,timedelta
from Admins.models import ApprovedUsers
from decouple import config
from django.contrib.auth.hashers import check_password

now = datetime.now()

key=config('secret')
algo=config('algos')

def Merge(dict1, dict2):
    res = {**dict1, **dict2}
    return res

def expiry_date():
    exp_date=datetime.now()+timedelta(3)
    password_expiry=datetime.now()+timedelta(30)
    return {"exp_date":exp_date.strftime('%d-%m-%Y'),"password_exp_date":password_expiry.strftime('%d-%m-%Y')}

class auths:
    def __init__(self,payload,enc):
        self.payload=payload
        self.enc=enc

    def encoded_jwt(self):
        return jwt.encode(Merge(self.payload,expiry_date()),key,algorithm=algo)

def Authorization(request,types):
    if request.META.get('HTTP_AUTHORIZATION'):
        
        header= request.META.get('HTTP_AUTHORIZATION')
        res = (header.split(' ', 1)[1])
        dec=jwt.decode(res, key, algorithms=algo)
        try:
            obj=ApprovedUsers.objects.filter(email=dec['uid'])
            obj2=obj.filter(password=dec['password'])
            if obj2.exists() and dec['role']==types:
                return dec['id']
            else:
                return 401

        except:
            return 401

    else:
        return 401



def Refresh_Token(token):

        dec=jwt.decode(token, key, algorithms=algo)

        today=now.strftime('%d-%m-%Y')
        print(today>dec['exp_date'],"refresh token")
        print('password exp date',30-(int(today[0:2])-int(dec['password_exp_date'][0:2])))
        email=dec['uid']
        password=dec['password']
        if ApprovedUsers.objects.exists():
            obj=ApprovedUsers.objects.filter(email=email)
            obj2=obj.filter(password=password)
            if dec['password_exp_date']>today:
                obj2.update(password='')
                return 'delete'
            print("token exp date",dec['exp_date'])
            if(today>dec['exp_date']):

                if obj2.exists():
                    data={
                        "uid":obj2.values('email')[0]['email'],
                        "password":obj2.values('password')[0]['password'],
                        "name":obj2.values('name')[0]['name'],
                        "id":obj.values('id_no')[0]['id_no'],
                        "role":obj.values('role')[0]['role'],
                        "phone":obj.values('phone')[0]['phone'],
                        "account_creates":obj.values('approved_at')[0]['approved_at'].strftime('%m/%d/%Y')
                    }
                    return jwt.encode(Merge(data,expiry_date()),key,algorithm=algo)





    
    
    


