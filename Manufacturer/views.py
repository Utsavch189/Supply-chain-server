import json
from sqlite3 import DatabaseError
from rest_framework.response import Response
from rest_framework.decorators import api_view
from Auth.Jwt import Authorization
from django.http import HttpResponse
from decouple import config
from datetime import date,datetime
from .Product_id import Product
from .models import *
from Admins.models import ApprovedUsers
import random

service=config('manufacturer_service')
now = datetime.now()

@api_view(['GET'])
def get_products(request):
    if  (Authorization(request,service))==401:
        return HttpResponse('Request Denied', status=401)
    obj=SetProduct.objects.filter(manufacturer_id=Authorization(request,service))
    stock_obj=ManufacturerStock.objects.filter(manufacturer_id=Authorization(request,service))
    if obj.exists():
        pro=[]
        for i in range(0,obj.count()):
            if stock_obj.exists():
                stock=stock_obj.filter(Product_id=obj.values('Product_id')[i]['Product_id'])
                if stock.exists():
                    data={
                        "name":obj.values('name')[i]['name'],
                        "id":obj.values('Product_id')[i]['Product_id'],
                        "price":obj.values('price')[i]['price'],
                        "desc":obj.values('description')[i]['description'],
                        "quant":stock.values('production_no')[0]['production_no']
                        }
                    pro.append(data)
                else:
                    data={
                    "name":obj.values('name')[i]['name'],
                    "id":obj.values('Product_id')[i]['Product_id'],
                    "price":obj.values('price')[i]['price'],
                    "desc":obj.values('description')[i]['description'],
                    "quant":0
                    }
                    pro.append(data)
            else:
                data={
                "name":obj.values('name')[i]['name'],
                "id":obj.values('Product_id')[i]['Product_id'],
                "price":obj.values('price')[i]['price'],
                "desc":obj.values('description')[i]['description'],
                "quant":0
                }
                pro.append(data)


        return Response({"data":pro,"status":200})


@api_view(['POST'])
def set_delete_update_products(request):
    if  (Authorization(request,service))==401:
        return HttpResponse('Request Denied', status=401)
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    
    msg=body['msg']
    p_id=body['p_id']
    name=body['name']
    price=body['price']
    desc=body['desc']

    main_obj=SetProduct.objects.all()
    if main_obj.filter(name=str(name).upper()).filter(price=price):
        id_p=main_obj.filter(name=str(name).upper()).filter(price=price).values('Product_id')[0]['Product_id']
        try:
            x=SetProduct(manufacturer_id=Authorization(request,service),name=str(name).upper(),price=price,description=desc,Product_id=id_p)
            x.save()
            return Response({"msg":"successfully added","status":200})
        except:
            return Response({"msg":"error!","status":400})
    
    else:
        if p_id and msg=='delete':
            objst=SetProduct.objects.filter(Product_id=p_id)
            objs=objst.filter(manufacturer_id=Authorization(request,service))
            objs.delete()
            return Response({"msg":"deleted","status":200})
        else:
            product_id=Product(name)
            objsss=SetProduct.objects.filter(name=name)
            objssss=objsss.filter(price=price)
            target_obj=objssss.filter(manufacturer_id=Authorization(request,service))
            if not p_id:
                if not target_obj.exists():
                    try:
                        x=SetProduct(manufacturer_id=Authorization(request,service),name=str(name).upper(),price=price,description=desc,Product_id=product_id)
                        x.save()
                        return Response({"msg":"successfully added","status":200})
                    except:
                        return Response({"msg":"error!","status":400})
                else:
                    return Response({"msg":"Duplicate product!","status":400})

            else:      
                objst=SetProduct.objects.filter(Product_id=p_id)
                objs=objst.filter(manufacturer_id=Authorization(request,service))

                try: 
                    objs.update(name=name)
                    objs.update(price=price)
                    objs.update(description=desc)
                    return Response({"msg":"successfully updated","status":200})
                except:
                    return Response({"msg":"error!","status":400})



@api_view(['POST'])
def entry_production(request):
    if  (Authorization(request,service))==401:
        return HttpResponse('Request Denied', status=401)

    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    p_id=body['p_id']
    product_no=body['product_no']

    obj=SetProduct.objects.filter(Product_id=p_id)
    target_obj=obj.filter(manufacturer_id=Authorization(request,service))
    name=target_obj.values('name')[0]['name']
    price=target_obj.values('price')[0]['price']
    desc=target_obj.values('description')[0]['description']

    a_obj=ManufacturerStock.objects.filter(Product_id=p_id)
    b_obj=a_obj.filter(manufacturer_id=Authorization(request,service))

    if not b_obj.exists():
        try:
            x=ManufacturerStock(manufacturer_id=Authorization(request,service),Product_id=p_id,name=name,price=price,description=desc,production_no=product_no,production_date=date.today())
            x.save()
            return Response({"msg":"successfully added","status":200})
        except:
            return Response({"msg":"error!","status":400})

    else:
        try:
            new_product_quant=str(int(b_obj.values('production_no')[0]['production_no'])+int(product_no))
            b_obj.update(production_no=new_product_quant)
            return Response({"msg":"successfully updated","status":200})
        except:
            return Response({"msg":"error!","status":400})




@api_view(['POST'])
def distribute(request):
    if  (Authorization(request,service))==401:
        return HttpResponse('Request Denied', status=401)

    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    dist_id=body['dist_id']
    manu_id=Authorization(request,service)
    p_id=body['p_id']
    quant=body['quant']
    
    ##product##
    obj=SetProduct.objects.filter(Product_id=p_id)
    target_obj=obj.filter(manufacturer_id=Authorization(request,service))
    price=target_obj.values('price')[0]['price']

    ##stockOFThatProduct##
    obb=ManufacturerStock.objects.filter(manufacturer_id=manu_id)
    obb1=obb.filter(Product_id=p_id)
    pre_stock=obb1.values('production_no')[0]['production_no']



    if(int(pre_stock)-int(quant)>=0):

        dist_obj1=Distribute.objects.filter(distributor_id=dist_id)
        if dist_obj1.exists():
            dist_obj2=dist_obj1.filter(manufacturer_id=manu_id)
            if dist_obj2.exists():
                dist_obj3=dist_obj2.filter(product_id=p_id)
                if dist_obj3.exists():
                    quant_val=dist_obj3.values('product_quantity')[0]['product_quantity']
                    price_val=dist_obj3.values('total_price')[0]['total_price']
                    dist_obj3.update(product_quantity=str(int(quant)+int(quant_val)))
                    dist_obj3.update(total_price=str(int(price_val)+(int(price)*int(quant))))
                    obb1.update(production_no=int(pre_stock)-int(quant))
                    return Response({"msg":"Distributed","status":200})
                else:
                    try:
                        x=Distribute(distributor_id=dist_id,product_id=p_id,manufacturer_id=manu_id,product_quantity=str(quant),total_price=str(int(quant)*int(price)),calculation_status=False,date=date.today())
                        x.save()
                        obb1.update(production_no=int(pre_stock)-int(quant))
                        return Response({"msg":"Distributed","status":200})
                    except:
                        return Response({"msg":"error!","status":400})

            else:
                try:
                    x=Distribute(distributor_id=dist_id,product_id=p_id,manufacturer_id=manu_id,product_quantity=str(quant),total_price=str(int(quant)*int(price)),calculation_status=False,date=date.today())
                    x.save()
                    obb1.update(production_no=int(pre_stock)-int(quant))
                    return Response({"msg":"Distributed","status":200})
                except:
                    return Response({"msg":"error!","status":400})


        else:
            try:
                x=Distribute(distributor_id=dist_id,product_id=p_id,manufacturer_id=manu_id,product_quantity=str(quant),total_price=str(int(quant)*int(price)),calculation_status=False,date=date.today())
                x.save()
                obb1.update(production_no=int(pre_stock)-int(quant))
                return Response({"msg":"Distributed","status":200})
            except:
                return Response({"msg":"error!","status":400})

    else:
        return Response({"msg":"Stock Limit exceed!","status":400})
            



@api_view(['POST'])
def a_user(request):
    if  (Authorization(request,service))==401:
        return HttpResponse('Request Denied', status=401)
    
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    u_id=body['u_id']
    users=[]
    history=[]
    alls=ApprovedUsers.objects.filter(id_no=u_id)

    data={
        'name':alls.values('name')[0]['name'],
        'phone':alls.values('phone')[0]['phone'],
        'email':alls.values('email')[0]['email'],
        'gender':alls.values('gender')[0]['gender'],
        'whatsapp':alls.values('whatsapp_no')[0]['whatsapp_no'],
        'role':alls.values('role')[0]['role'],
        'id':alls.values('id_no')[0]['id_no'],
        }
    users.append(data)

    colors=['#5780c1','#34568b','#6a8ec8','#ff8a80','#ff5b4d','#ffb9b3','#adc982','#88b04b','#dce8c9','#783a6d','#cd98c3','#b565a7','#c1253c','#fbeaec']
    
    proObj=SetProduct.objects.all()
    dist_obj=Distribute.objects.filter(distributor_id=u_id)
    my_obj=dist_obj.filter(manufacturer_id=Authorization(request,service))
    for i in range(0,my_obj.count()):
        num=random.randint(0,13)
        p_name=proObj.filter(Product_id=my_obj.values('product_id')[i]['product_id'])
        details={
            "name":p_name.values('name')[0]['name'],
            "quant":int(my_obj.values('product_quantity')[i]['product_quantity']),
            "color":colors[num]
        }
        history.append(details)
       

    return Response({"user":users,"history":history})


@api_view(['POST'])
def DayByDayEntry(request):
    if  (Authorization(request,service))==401:
        return HttpResponse('Request Denied', status=401)

    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    p_id=body['p_id']
    product_no=body['product_no']

    obj=SetProduct.objects.filter(Product_id=p_id)
    target_obj=obj.filter(manufacturer_id=Authorization(request,service))
    name=target_obj.values('name')[0]['name']

    dayBYdayProOBJ=DayByDayProducts.objects.filter(product_id=p_id)
    dayBYdayProOBJ1=dayBYdayProOBJ.filter(manufacturer_id=Authorization(request,service)).filter(date=date.today())
    
    if dayBYdayProOBJ1.exists():  
        try:
            pre_quant=dayBYdayProOBJ1.values('product_quantity')[0]['product_quantity']
            dayBYdayProOBJ1.update(product_quantity=str(int(pre_quant)+int(product_no)))
            return Response({"msg":"successfully added in daybyday record","status":200})
        except:
            return Response({"msg":"error in added in daybyday record","status":400})
      
    else:
        try:
            y=DayByDayProducts(product_id=p_id,manufacturer_id=Authorization(request,service),product_name=name,product_quantity=product_no,date=date.today())
            y.save()
            return Response({"msg":"successfully created in daybyday record","status":200})
        except:
            return Response({"msg":"error in creation in daybyday record","status":400})



@api_view(['POST'])
def post_dayBYdayDistribute(request):
    if  (Authorization(request,service))==401:
        return HttpResponse('Request Denied', status=401)

    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    dist_id=body['dist_id']
    manu_id=Authorization(request,service)
    p_id=body['p_id']
    quant=body['quant']

    main_obj=DayByDayProductsDistribute.objects.filter(product_id=p_id).filter(manufacturer_id=manu_id).filter(distributor_id=dist_id).filter(date=date.today())
    if main_obj.exists():
        try:
            pre_quant=main_obj.values('product_quantity')[0]['product_quantity']
            main_obj.update(product_quantity=str(int(quant)+int(pre_quant)))
            return Response({"msg":"successfully added in daybyday record","status":200})
        except:
            return Response({"msg":"error in added in daybyday record","status":400})
        

    else:
        try:
            y=DayByDayProductsDistribute(product_id=p_id,manufacturer_id=manu_id,product_quantity=quant,distributor_id=dist_id,date=date.today())
            y.save()
            return Response({"msg":"successfully created in daybyday record","status":200})
        except:
            return Response({"msg":"error in creation in daybyday record","status":400})



@api_view(['GET'])
def get_dayBYdayDistribute(request):
    if  (Authorization(request,service))==401:
        return HttpResponse('Request Denied', status=401)

    main_obj=DayByDayProductsDistribute.objects.filter(manufacturer_id=Authorization(request,service))
    if main_obj.exists():
        head=['Date','ProductID','ProductName','DistributorName','Quantity']
        tittle=[]
        data=[]
        for i in range(0,main_obj.count()):
            a_tittle=[main_obj.values('date')[i]['date']]
            tittle.append(a_tittle)

            p_id=main_obj.values('product_id')[i]['product_id']
            p_name=SetProduct.objects.filter(Product_id=p_id).values('name')[0]['name']
            dist_id=main_obj.values('distributor_id')[i]['distributor_id']
            dist_name=ApprovedUsers.objects.filter(id_no=dist_id).values('name')[0]['name']
            p_quant=main_obj.values('product_quantity')[i]['product_quantity']
            a_data=[p_id,p_name,dist_name,p_quant]
            data.append(a_data)
        return Response({"head":head,"data":data,"tittle":tittle,"status":200})
    else:
        return Response({"msg":"no data!"})




@api_view(['GET'])
def get_DayByDayEntry(request):
    if  (Authorization(request,service))==401:
        return HttpResponse('Request Denied', status=401)

    colors=['#5780c1','#34568b','#6a8ec8','#ff8a80','#ff5b4d','#ffb9b3','#adc982','#88b04b','#dce8c9','#783a6d','#cd98c3','#b565a7','#c1253c','#fbeaec']
    main_obj=DayByDayProducts.objects.filter(manufacturer_id=Authorization(request,service)).filter(date=date.today())
    stats=[]
    if main_obj.exists():
        for i in range(0,main_obj.count()):
            num=random.randint(0,13)
            data={
                "name":main_obj.values('product_name')[i]['product_name'],
                "count":main_obj.values('product_quantity')[i]['product_quantity'],
                "color":colors[num]
            }
            stats.append(data)
        return Response({"data":stats,"status":200})
    else:
        return Response({"data":stats,"status":200})


