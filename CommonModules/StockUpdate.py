
from Manufacturer.models import SetProduct,Distribute
from datetime import date
from Distributor.models import *
from Retailer.models import *

class Stock:
    def __init__(self,userid):
        self.userid=userid


        
    def updatefordistributor(self):
        obj=Distribute.objects.filter(distributor_id=self.userid).filter(calculation_status=False)
        if obj.exists():
            for i in range(0,obj.count()):
                product_id=obj.values('product_id')[i]['product_id']
                manufacturer_id=obj.values('manufacturer_id')[i]['manufacturer_id']
                product_quantity=obj.values('product_quantity')[i]['product_quantity']
                total_price=obj.values('total_price')[i]['total_price']
                price_per_product=str(int(total_price)/int(product_quantity))
                product_name=SetProduct.objects.filter(Product_id=product_id).values('name')[0]['name']
                if(DistributorStock.objects.filter(product_id=product_id).filter(distributor_id=self.userid).exists()):
                    sub_obj=DistributorStock.objects.filter(product_id=product_id).filter(distributor_id=self.userid)
                    sub_obj.update(product_quantity=product_quantity)
                    sub_obj.update(total_price=total_price)
                    sub_obj.update(price_per_product=price_per_product)
                else:
                    try:
                        x=DistributorStock(product_id=product_id,product_name=product_name,manufacturer_id=manufacturer_id,distributor_id=self.userid,product_quantity=product_quantity,total_price=total_price,price_per_product=price_per_product,date=date.today())
                        x.save()
                    except:
                        pass
            obj.update(calculation_status=True)

    def updateforretailer(self):
        obj=DistributeToRetailer.objects.filter(retailer_id=self.userid).filter(calculation_status=False)
        if obj.exists():
            for i in range(0,obj.count()):
                product_id=obj.values('product_id')[i]['product_id']
                distributor_id=obj.values('distributor_id')[i]['distributor_id']
                product_quantity=obj.values('product_quantity')[i]['product_quantity']
                total_price=obj.values('total_price')[i]['total_price']
                price_per_product=str(int(total_price)/int(product_quantity))
                product_name=SetProduct.objects.filter(Product_id=product_id).values('name')[0]['name']
                if(RetailerStock.objects.filter(product_id=product_id).filter(retailer_id=self.userid).exists()):
                    sub_obj=RetailerStock.objects.filter(product_id=product_id).filter(retailer_id=self.userid)
                    sub_obj.update(product_quantity=product_quantity)
                    sub_obj.update(total_price=total_price)
                    sub_obj.update(price_per_product=price_per_product)
                else:
                    try:
                        x=RetailerStock(product_id=product_id,product_name=product_name,distributor_id=distributor_id,retailer_id=self.userid,product_quantity=product_quantity,total_price=total_price,price_per_product=price_per_product,date=date.today())
                        x.save()
                    except:
                        pass
            obj.update(calculation_status=True)
