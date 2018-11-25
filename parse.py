import re
from datetime import datetime
from datetime import timedelta
querylist =  []   
queryeraser =  []

    

        
def parseQuery(text):
    global querylist
    dateRe = '(\ {1,}date\{0,}[<>]{0,1}[=]{0,1}\d{2})[/](\d{2})[/](\d{4}\ {0,}[a-zA-Z0-9-_]{0,})'
    priceRe = '(\ {1,}price\ {0,}[<>]{0,1}[=]{0,1}\ {0,}[a-zA-Z0-9-_]{0,})'
    locationRe = '(\ {1,}location\ {0,}[=]{0,1}\ {0,}[a-zA-Z0-9-_]{0,})'
    catRe = '(\ {1,}cat\ {0,}[=]{0,1}\ {0,}[a-zA-Z0-9-_]{0,})'
    captureQuery(dateRe, text)
    captureQuery(locationRe, text)
    captureQuery(priceRe, text)
    captureQuery(catRe, text)
    captureRest(text) 
    return querylist

def captureQuery(Re, text):
    global queryeraser, querylist
    captures = re.findall(Re, text)
    for i in captures:
        queryeraser.append(i)
        i = i.replace(" ","")
        querylist.append(i)


def captureRest(text):
    global queryeraser, querylist
    strre = '(^\w{0,1}[^<>=]$)'
    for i in queryeraser:
        text = text.replace(i,"")
    text = text.split(" ")

    for i in text:
        querylist.append(i)
 
def dateadd(date):
    date1 = []
    year,month,day =date.split("/")
    d=str(datetime(int(year), int(month), int(day)) + timedelta(days=1))
    d=d[0:10]
    d=d.replace("-","/")
    return d

def datesub(date):
    date1 = []
    year,month,day =date.split("/")
    d=str(datetime(int(year), int(month), int(day)) - timedelta(days=1)) 
    d=d[0:10]
    d=d.replace("-","/")    
    return d 

def mindate(dates):
    datelist = []
    for date in dates:
        year,month,day =date.split("/")
        d=str(datetime(int(year), int(month), int(day))) 
        d=d[0:10]
        d=d.replace("-","/") 
        datelist.append(d)
    m=min(datelist)
    return m   

def maxdate(dates):
    datelist = []
    for date in dates:
        year,month,day =date.split("/")
        d=str(datetime(int(year), int(month), int(day))) 
        d=d[0:10]
        d=d.replace("-","/") 
        datelist.append(d)
    m=max(datelist)
    return m  

def getidealcond(text):
    global queryeraser, querylist
    finallist = set()
    idealprice1 = []
    idealprice2 = []
    idealdate1 = []
    idealdate2 = []    
    oldlist = parseQuery(text)
    price1 = re.compile("price\>[0-9]")
    price2 = re.compile("price\<[0-9]")
    price3 = re.compile("price\>=[0-9]")
    price4 = re.compile("price\<=[0-9]")   
    date1 = re.compile("date\>\\d{4}\/\d{2}\/\d{2}")
    date2 = re.compile("date\<\\d{4}\/\d{2}\/\d{2}")
    date3 = re.compile("date\>=\\d{4}\/\d{2}\/\d{2}")
    date4 = re.compile("date\<=\\d{4}\/\d{2}\/\d{2}")   
    

    list1 =  set()
    list2 =  set()
    list3 =  set()
    list4 =  set()    
    for i in oldlist:
        
        if((price1.match(i)) or price3.match(i)):
            idealprice1.append(i)
            
            for i in idealprice1:
                i = i.split(">")
                grequal = re.compile("=[0-9]")
                
                if(grequal.match(i[1])):
                    
                    line = int(re.sub('=', '', i[1]))
                    
                    line = line-1
                
                    list1.add(line)
                else:    
                    list1.add(int(i[1]))
        
        elif(price2.match(i) or price4.match(i)):
            idealprice2.append(i)
            for i in idealprice2:
                i = i.split("<")
                lsequal = re.compile("=[0-9]")
               
                if(lsequal.match(i[1])):
                    
                    line = int(re.sub('=', '', i[1]))
                    
                    line = line+1
                    
                    list2.add(line)
                else:
                    list2.add(int(i[1]))
        elif(date1.match(i) or date3.match(i)):
            idealdate1.append(i)
            for i in idealdate1:
                i = i.split(">")
                dgequal = re.compile("=\\d{4}\/\d{2}\/\d{2}")
                
           
                if(dgequal.match(i[1])):
                    
                    line = re.sub('=', '', i[1])
                    
                    line = dateadd(line)
                    
                    list3.add(line)
                else:
                    list3.add(int(i[1]))
        elif(date2.match(i) or date4.match(i)):
            idealdate2.append(i)
            for i in idealdate2:
                i = i.split("<")
                dlequal = re.compile("=\\d{4}\/\d{2}\/\d{2}")
               
                if(dlequal.match(i[1])):
                    
                    line = re.sub('=', '', i[1])
                    
                    line = datesub(line)
                    
                    list4.add(line)
                else:
                    list4.add(int(i[1]))        
                    
        else:
            finallist.add(i)  
                
 
                             
    list1= list(list1)   
    
    
       
    if list1 != []:        
        m = max(list1) 
       
        for i in idealprice1:
            if "price>"+str(m)==i or  "price>="+ str(m+1)==i :
                finallist.add(i)            
                        
        
    list2 = list(list2)      
    if list2!= []:
        n = min(list2)
       
        for j in idealprice2:
            if "price<"+str(n)==j or "price<="+ str(n-1)==j :
                
                finallist.add(j)
    
    list3 = list(list3) 
    
    if list3!= []:
        k = mindate(list3)
        
       
        for j in idealdate1:
            if "date>"+str(k)==j or "date>="+ datesub(k)==j :
                
                finallist.add(j)
                
    list4 = list(list4) 
    
    if list4!= []:
        k = maxdate(list4)
        
       
        for j in idealdate2:
            if "date<"+str(k)==j or "date<="+ dateadd(k)==j :
                
                finallist.add(j)
    
    finallist = list(finallist) 
    
    return finallist

def main():
    print("Please enter your query, type exit to quit.")
    while True:
        text = input()
        text = text.strip(" ")
        text = " "+text 
        if text == "exit":
            break
        else:
            print(getidealcond(text))
            break             
    
if __name__ == "__main__":        
    main() 
'''
test with:
  date<=2018/11/07  date<=2018/11/05  price >= 41 price > 30 price > 20  price < 33  price <= 30 price < 40  location = edmonton cat=art-collectibles camera
 '''
