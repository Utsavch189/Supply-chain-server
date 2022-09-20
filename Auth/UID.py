import string
import random
from .models import *

def creates():
        res = ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k=25))
        if Register.objects.exists():
            obb=Register.objects.filter(id_no=res)
            if obb.exists():
                creates()
            else:
                return res
        else:
            return res
   
