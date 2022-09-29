import json
from rest_framework.response import Response
from rest_framework.decorators import api_view
from Auth.Jwt import Authorization
from .models import ApprovedUsers,DeletedUsers
from Auth.models import Register
from datetime import date
from Auth.Mail import approve_mail,removeUser_mail,Reapprove_mail
from django.http import HttpResponse
from decouple import config
from Manufacturer.models import SetProduct,Distribute
import random

service=config('admin_service')


@api_view(['GET'])
def requests(request):
    if  (Authorization(request,service))==401:
        return HttpResponse('Request Denied', status=401)
    
    
    users=[]
    alls=Register.objects.all()
    if alls.exists():
        for i in range(0,alls.count()):
            data={
                'name':alls.values('name')[i]['name'],
                'phone':alls.values('phone')[i]['phone'],
                'email':alls.values('email')[i]['email'],
                'gender':alls.values('gender')[i]['gender'],
                'whatsapp':alls.values('whatsapp_no')[i]['whatsapp_no'],
                'role':alls.values('role')[i]['role'],
                'id':alls.values('id_no')[i]['id_no'],
            }

        
       
            users.append(data)
        return Response(users)

    return Response({"msg":"no data"})
    
    


@api_view(['GET'])
def approved_users(request):
        if  (Authorization(request,service))==401:
            return HttpResponse('Request Denied', status=401)
        users=[]
        alls=ApprovedUsers.objects.all()
        if alls.exists():
            for i in range(0,alls.count()):

                data={
                    'name':alls.values('name')[i]['name'],
                    'phone':alls.values('phone')[i]['phone'],
                    'email':alls.values('email')[i]['email'],
                    'gender':alls.values('gender')[i]['gender'],
                    'whatsapp':alls.values('whatsapp_no')[i]['whatsapp_no'],
                    'role':alls.values('role')[i]['role'],
                    'id':alls.values('id_no')[i]['id_no'],
                }

        
                if not data['role']=='Admin':
                    users.append(data)
            return Response(users)

        return Response({"msg":"no data"})
    


@api_view(['GET'])
def deletedusers_users(request):
        if  (Authorization(request,service))==401:
            return HttpResponse('Request Denied', status=401)
        users=[]
        alls=DeletedUsers.objects.all()
        if alls.exists():
            for i in range(0,alls.count()):
                data={
                    'name':alls.values('name')[i]['name'],
                    'phone':alls.values('phone')[i]['phone'],
                    'email':alls.values('email')[i]['email'],
                    'gender':alls.values('gender')[i]['gender'],
                    'whatsapp':alls.values('whatsapp_no')[i]['whatsapp_no'],
                    'role':alls.values('role')[i]['role'],
                    'id':alls.values('id_no')[i]['id_no'],
                }

        
       
                users.append(data)
            return Response(users)

        return Response({"msg":"no data"})
    


@api_view(['POST'])
def approve_a_user(request):
        if  (Authorization(request,service))==401:
            return HttpResponse('Request Denied', status=401)
    
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        id_no=body['id_no']
        obj=Register.objects.filter(id_no=id_no)
        if obj.exists():
            name=obj.values('name')[0]['name']
            phone=obj.values('phone')[0]['phone']
            email=obj.values('email')[0]['email']
            password=obj.values('password')[0]['password']
            gender=obj.values('gender')[0]['gender']
            whatsapp=obj.values('whatsapp_no')[0]['whatsapp_no']
            role=obj.values('role')[0]['role']
            idd=obj.values('id_no')[0]['id_no']
            print(name)
            try:
                x=ApprovedUsers(name=name,phone=phone,email=email,password=password,gender=gender,whatsapp_no=whatsapp,role=role,id_no=idd,approved_at=date.today())
                x.save()
                obj.delete()
                approve_mail(email,name)
                return Response({"msg":"successfully created!","status":200})
            except:
                return Response({"msg":"error!","status":400})

        
    


@api_view(['POST'])
def delete_a_user(request):
        if  (Authorization(request,service))==401:
            return HttpResponse('Request Denied', status=401)
        
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        id_no=body['id_no']
        obj=Register.objects.filter(id_no=id_no)
        if obj.exists():
           
            name=obj.values('name')[0]['name']
            phone=obj.values('phone')[0]['phone']
            email=obj.values('email')[0]['email']
            password=obj.values('password')[0]['password']
            gender=obj.values('gender')[0]['gender']
            whatsapp=obj.values('whatsapp_no')[0]['whatsapp_no']
            role=obj.values('role')[0]['role']
            idd=obj.values('id_no')[0]['id_no']
            
            try:
                x=DeletedUsers(name=name,phone=phone,email=email,password=password,gender=gender,whatsapp_no=whatsapp,role=role,id_no=idd,deleted_at=date.today())
                x.save()
                obj.delete()
                
                removeUser_mail(email,name)
               
                return Response({"msg":"successfully removed!","status":200})
            except:
                return Response({"msg":"error!","status":400})
            
        elif (ApprovedUsers.objects.filter(id_no=id_no).exists()):
            obj=ApprovedUsers.objects.filter(id_no=id_no)
            name=obj.values('name')[0]['name']
            phone=obj.values('phone')[0]['phone']
            email=obj.values('email')[0]['email']
            password=obj.values('password')[0]['password']
            gender=obj.values('gender')[0]['gender']
            whatsapp=obj.values('whatsapp_no')[0]['whatsapp_no']
            role=obj.values('role')[0]['role']
            idd=obj.values('id_no')[0]['id_no']
            
            try:
                x=DeletedUsers(name=name,phone=phone,email=email,password=password,gender=gender,whatsapp_no=whatsapp,role=role,id_no=idd,deleted_at=date.today())
                x.save()
                obj.delete()

                removeUser_mail(email,name)

                return Response({"msg":"successfully removed!","status":200})
            except:
                return Response({"msg":"error!","status":400})
            


@api_view(['POST'])
def reapprove_a_user(request):
        if  (Authorization(request,service))==401:
            return HttpResponse('Request Denied', status=401)
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        id_no=body['id_no']
        obj=DeletedUsers.objects.filter(id_no=id_no)
        if obj.exists():
            name=obj.values('name')[0]['name']
            phone=obj.values('phone')[0]['phone']
            email=obj.values('email')[0]['email']
            password=obj.values('password')[0]['password']
            gender=obj.values('gender')[0]['gender']
            whatsapp=obj.values('whatsapp_no')[0]['whatsapp_no']
            role=obj.values('role')[0]['role']
            idd=obj.values('id_no')[0]['id_no']
            try:
                x=ApprovedUsers(name=name,phone=phone,email=email,password=password,gender=gender,whatsapp_no=whatsapp,role=role,id_no=idd,approved_at=date.today())
                x.save()
                obj.delete()
                Reapprove_mail(email,name)
                return Response({"msg":"successfully removed!","status":200})
            except:
                return Response({"msg":"error!","status":400})

        
@api_view(['GET'])
def numbers_of_users(request):
    if  (Authorization(request,service))==401:
            return HttpResponse('Request Denied', status=401)
 
    obj=ApprovedUsers.objects.filter(role='Manufacturer')
    obj1=ApprovedUsers.objects.filter(role='Retailer')
    obj2=ApprovedUsers.objects.filter(role='Distributor')

    colors1=['#5780c1','#34568b','#6a8ec8','#ff8a80','#ff5b4d']
    colors2=['#ffb9b3','#adc982','#88b04b','#dce8c9','#783a6d']
    colors3=['#cd98c3','#b565a7','#c1253c','#fbeaec',"#556B2F"]
    num1=random.randint(0,4)
    num2=random.randint(0,4)
    num3=random.randint(0,4)

    data=[
        {'count':obj.count(),"name":"Manufacturer","color":colors1[num1]},
        {'count':obj2.count(),"name":"Distributor","color":colors2[num2]},
        {'count':obj1.count(),"name":"Retailer","color":colors3[num3]}
    ]

    return Response(data)



