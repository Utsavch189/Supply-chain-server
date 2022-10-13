import string
import random
from .models import *
from Admins.models import ApprovedUsers

def creates():
        res = ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k=25)).upper()
        if Register.objects.exists() or ApprovedUsers.objects.exists():
            
            if Register.objects.filter(id_no=res).exists() or ApprovedUsers.objects.filter(id_no=res).exists():
                creates()
            else:
                return res
        else:
            return res
   
