from datetime import datetime
from .models import SetProduct
def Product(name):
    now = datetime.now()
    year = now.strftime("%Y")
    month = now.strftime("%m")
    day = now.strftime("%d")
    
    token= str(name[0]).upper()+str(day)+str(month)+str(year)
    obj=SetProduct.objects.filter(Product_id=token)
    if not obj.exists():
        return token
    else:
        i=0
        length=len(name)
        while(length>0):
            token= str(name[0]).upper()+str(name[i]).upper()+str(day)+str(month)+str(year)
            if not obj.exists():
                return token
            else:
                i+=1
                length-=1