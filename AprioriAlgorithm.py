import csv

import matplotlib.pyplot as pt
from tqdm import tqdm

with open('new_data.csv', newline='') as f:
    reader = csv.reader(f)
    data = list(reader)


L=[]
nT=0;
for i in data:
    nT=nT+1;
    if(nT>75000):
        break
    templist=[]
    for j in i:
        if(j!="unknown"):
            templist.append(j)
    
    L.append(templist)
print(L)
print(len(L))


s=int(input("Enter Support count  "))

FP=[] #List to store frequent patterns

def autopct_format(values):
    def my_format(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{v:d}'.format(v=val)
    return my_format

C1=[]
for i in L:
    for j in i:
        if(C1.count(j)==0):
            C1.append(j)
C1.sort()            

D={}

for i in C1:
    D[i]=0

for i in L:
    for j in i:
        D[j]=D[j]+1  #calculate support count of each item
        


for i in D.copy():
    if D[i]<s:
        del D[i]  #Deleting the items on support count

        
FP.append(D)
#C1 and L1
height=[]
label=[]
for i in FP[0].keys():
    print(i,"---->",FP[0][i])
    height.append(FP[0][i])
    label.append(i)
total = sum(height)
pt.title("Level -- 1 Candidate List\n\n\n")
pt.pie(height,labels=label,shadow=True,autopct=autopct_format(height),radius=1.0,labeldistance=1.3)

pt.legend(loc='center left', bbox_to_anchor=(1.8, 0.8))

pt.show()
#Level 2 to Level N

count=1

while(True):
    count=count+1
    D1={} #temporary dictionary to store items of each level
    B=list(FP[len(FP)-1]) #previous level itemset
    progressbar = tqdm(range(0,len(B)),desc="Phase-1 Ariori")
    for i in progressbar:
        for j in range(i,len(B)-1):
            ola=list(set((B[i]+","+B[j+1]).split(","))) #possible item patterns in respective level
            ola.sort()
            if len(ola) <=count:
                olam=""
                for k in ola:
                    olam=olam+k+","
                D1[olam[0:-1]]=0
                    
   

    for i in D1.copy():
        for j in L:
            if(all(x in j for x in i.split(","))):
                D1[i]=D1[i]+1   #support count
            
    

    for i in D1.copy():
        if D1[i]<s:
            del D1[i]   #delete items based on support count
    if len(D1)==0:
        break
    FP.append(D1) #adding each level item set to FP
#print(FP)

for i in FP:
    #height=[]
   # label=[]
    print("\n\nLEVEL  -- ",(FP.index(i)+1))
    print("-------------------------------------------------------------------------------------------------------------\n")
    for j in i.keys():
        print(j,"---->",i[j])
      #  height.append(i[j])
     #   label.append(j)
    #pt.pie(height,labels=label,shadow=True,autopct=autopct_format(height),radius=1.5,labeldistance=1.4)
    
    #pt.savefig("level"+str((FP.index(i)+1))+".jpg", bbox_inches='tight', pad_inches=0)
    #pt.legend(loc='center left', bbox_to_anchor=(2.0, 0.8))
    #pt.show()
    
    
print("Frequent pattern obtained are")
#print(FP[len(FP)-1])

for i in FP[len(FP)-1].keys():
    print(i,"---->",FP[len(FP)-1][i])
 
    
    
    
def pset(myset):   # powerset function to find possible association rules
    
    if not myset: # Empty list -> empty set
        return [set()]

    r = []
    for y in myset:
        sy = set((y,))
        for x in pset(myset - sy):
            if x not in r:
                r.extend([x, x|sy])
    return r

    
#Association rules for obtained frequent patterns
#X-->Y
AR={}  
AR=FP[len(FP)-1]
ARL=[]
for i in AR.copy():
    rectemp=i.split(",")
    ARL.append(rectemp) #storing eac pattern

DRL=[]#To store left side of AR : (X)
SRL=[]#To store right side of AR : (Y)
progressbar = tqdm(ARL,desc="\n\n\nPhase-2 Ariori")
for k in progressbar:
    s=set()
    s=pset(set(k))#power set for each pattern

    s.pop(0)#delete empty set
    s.pop()

    p=set(k)



    for i in range(0,len(s)):
        DRL.append(list(p.difference(s[i])))
        DRL[i]=list(DRL[i])
        s[i]=list(s[i])

    for i in s:
        SRL.append(i)    
  
    
vc=[]#frequency(X)
vc1=[]#frequency(X,Y)
for i in range(0,len(SRL)):
    vc.append(0)
    vc1.append(0)

for i in range(0,len(SRL)):
    for j in L:
        if(set(SRL[i]).issubset(set(j))):
            vc[i]=vc[i]+1   #calculate freq(X)
            m=set()
            n=set()
            m=set(DRL[i])
            n=set(SRL[i])
            o=m.union(n)
            #print(o)
            if(o.issubset(set(j))):
                vc1[i]=vc1[i]+1    # calculate freq(X,Y)
#print("Values of [(freq(X),freq(X,Y))] for all Association rules:\n")                
#print([(x,y)for x,y in zip(vc,vc1)])


con=int(input("Enter confidence %  "))
con=con/100
print("Valid Associative Rules :\n\n")

for i in range(0,len(vc)):  #valid association rules based on confidence
    if vc1[i]/vc[i] >con :
        print(SRL[i],"--->",DRL[i],"   ("+str((vc1[i]/vc[i])*100)+")")


