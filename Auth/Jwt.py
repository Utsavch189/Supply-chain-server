from logging import exception
import jwt
from datetime import datetime,timedelta
from Admins.models import ApprovedUsers

from decouple import config

key=config('secret')
algo=config('algos')

def Merge(dict1, dict2):
    res = {**dict1, **dict2}
    return res

def expiry_date():
    exp_date=datetime.now()+timedelta(3)
    return {"exp_date":exp_date.strftime('%d-%m-%Y')}

class auths:
    def __init__(self,payload,enc):
        self.payload=payload
        self.enc=enc

    def encoded_jwt(self):
        return jwt.encode(Merge(self.payload,expiry_date()),key,algorithm=algo)

def Authorization(request,types):
    header= request.META.get('HTTP_AUTHORIZATION')
    res = (header.split(' ', 1)[1])
    dec=jwt.decode(res, key, algorithms=algo)

    try:
        obj=ApprovedUsers.objects.filter(email=dec['uid'])
        obj_r=obj.filter(password=dec['password'])
        if(obj_r) and dec['role']==types:
            return dec
        else:
            raise Exception("Invalid")

    except:
        raise Exception("Error")


    
    
    


