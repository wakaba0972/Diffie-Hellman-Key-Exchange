from random import randint, getrandbits

def convert(p):
    s=0
    while p&1==0:
        s+=1; p>>=1
    return s, p

def Miller_Rabin(p):
    if p<2: return False
    if p==2: return True
    if p&1==0: return False
    
    s, d=convert(p-1)
    a=randint(2,p-1)
    ad=pow(a,d,p)
    if ad==1 or ad==p-1: return True
    for r in range(s-1):
        ad=pow(ad,2,p)
        if ad==p-1: return True
        if not (ad == p-1 or ad == 1): return False
    return False
        
def Bprime(bits,k=100):
    while 1:
        p=getrandbits(bits)
        if p&1==0: p+=1
        for i in range(k):
            b=Miller_Rabin(p)
            if b==False: break
            if i==k-1 and b: return p
