import json
from rest_framework.response import Response
from rest_framework.decorators import api_view
from Auth.Jwt import Authorization
from .models import ApprovedUsers,DeletedUsers
from Auth.models import Register
from datetime import date
from Auth.Mail import approve_mail,removeUser_mail,Reapprove_mail


@api_view(['POST'])
def requests(request):
    res=(Authorization(request,'Admin'))
    if res:
        print(res)
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
    return Response({"msg":"not authorized","status":401})
    


@api_view(['POST'])
def approved_users(request):
    res=(Authorization(request,'Admin'))
    if res:
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

        
       
                users.append(data)
            return Response(users)

        return Response({"msg":"no data"})
    return Response({"msg":"not authorized","status":401})


@api_view(['POST'])
def deletedusers_users(request):
    res=(Authorization(request,'Admin'))
    if res:
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
    return Response({"msg":"not authorized","status":401})


@api_view(['POST'])
def approve_a_user(request):
    res=(Authorization(request,'Admin'))
    if res:
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
                x=ApprovedUsers(name=name,phone=phone,email=email,password=password,gender=gender,whatsapp_no=whatsapp,role=role,id_no=idd,approved_at=date.today())
                x.save()
                approve_mail(email,name)
                return Response({"msg":"successfully created!","status":200})
            except:
                return Response({"msg":"error!","status":400})

        
    return Response({"msg":"not authorized","status":401})


@api_view(['POST'])
def delete_a_user(request):
    res=(Authorization(request,'Admin'))
    if res:
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        id_no=body['id_no']
        obj=ApprovedUsers.objects.filter(id_no=id_no)
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
                x=DeletedUsers(name=name,phone=phone,email=email,password=password,gender=gender,whatsapp_no=whatsapp,role=role,id_no=idd,approved_at=date.today())
                x.save()
                obj.delete()
                removeUser_mail(email,name)
                return Response({"msg":"successfully removed!","status":200})
            except:
                return Response({"msg":"error!","status":400})

        
    return Response({"msg":"not authorized","status":401})


@api_view(['POST'])
def reapprove_a_user(request):
    res=(Authorization(request,'Admin'))
    if res:
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

        
    return Response({"msg":"not authorized","status":401})
