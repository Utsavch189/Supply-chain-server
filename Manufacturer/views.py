import json
from rest_framework.response import Response
from rest_framework.decorators import api_view
from Auth.Jwt import Authorization
from django.http import HttpResponse
from decouple import config
from datetime import date
from .Product_id import Product
from .models import *
from Admins.models import ApprovedUsers

service=config('manufacturer_service')

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


        return Response({"data":pro,"status":200})


@api_view(['POST'])
def set_delete_update_products(request):
    if  (Authorization(request,service))==401:
        return HttpResponse('Request Denied', status=401)
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    
    msg=body['msg']
    p_id=body['p_id']
    

    if p_id and msg=='delete':
        objst=SetProduct.objects.filter(Product_id=p_id)
        objs=objst.filter(manufacturer_id=Authorization(request,service))
        objs.delete()
        return Response({"msg":"deleted","status":200})
    else:
        name=body['name']
        price=body['price']
        desc=body['desc']
        product_id=Product(name)
        objsss=SetProduct.objects.filter(name=name)
        objssss=objsss.filter(price=price)
        target_obj=objssss.filter(manufacturer_id=Authorization(request,service))
        if not p_id:
            if not target_obj.exists():
                try:
                    x=SetProduct(manufacturer_id=Authorization(request,service),name=name,price=price,description=desc,Product_id=product_id)
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

    try:
        x=Distribute(distributor_id=dist_id,product_id=p_id,manufacturer_id=manu_id,product_quantity=str(quant),total_price=str(int(quant)*int(price)),calculation_status=False,date=date.today())
        x.save()
        return Response({"msg":"Distributed","status":200})
    except:
        return Response({"msg":"error!","status":400})





