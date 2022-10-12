def sortObj(a,key):
    l=len(a)
    if l>5:
        a.sort(key=lambda x:x[key])
        res=[]
        res.append(a[l-1])
        res.append(a[l-2])
        res.append(a[l-3])
        res.append(a[l-4])
        res.append(a[l-5])
        return res
    else:
        return a