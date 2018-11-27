from bsddb3 import db
import re
import sys
from datetime import datetime
from datetime import timedelta

querylist =  []   
queryeraser =  []
resultlist = set()

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

def fetch(text):
    global  querylist
    qlist= getidealcond(text)
    pr = 'price'
    da = 'date'
    lo = 'location'
    ca = 'cat'
    
    
    for a in qlist[:]:
        if a.startswith(pr):
            qlist.remove(a)
            pricefunct(a)
            
    for b in qlist[:]:
        if b.startswith(da):
            qlist.remove(b)
            date_cat_loc(b,0,0) 
            
    for c in qlist[:]:
        if c.startswith(lo):
            qlist.remove(c)
            date_cat_loc(0,0,c)
            
    for d in qlist[:]:
        if d.startswith(ca):
            qlist.remove(d)
            date_cat_loc(0,d,0)

    for e in qlist:
        if e != '':
            te = e
            terms(te)
            
def terms(te):
    global resultlist 
    termsDB = db.DB()
    termsDB.open('te.idx',None,db.DB_BTREE,db.DB_CREATE)
        
    cursor = termsDB.cursor()
    
    term1 = re.compile("[A-Za-z0-9]+[/%]")
    
    if te != 0:
        if(term1.match(te)):
            firstterm = re.sub("%",'',te)
            #print('firstterm', firstterm)
        
            matching = False    
            if firstterm != 0:
                matching = True
                firstterm1 = firstterm[:-1]
                end = len(firstterm1)
                n = firstterm[:end]
            result = cursor.set_range(n.encode("utf-8"))
            
        
            if(result != None):
                #print("List of found descriptions:")
            
                while(result != None):
                    #Checking the end condition: If the student's name comes after(or equal to) Ending_Name
                    if(str(result[0].decode("utf-8")[:end])!=n): 
                        break
                    
                    term = (str(result[0].decode("utf-8")) + ": " + str(result[1].decode("utf-8")))
                    resultlist.add(term)
                    result = cursor.next() 
            #else:
                #print("No ranges were found")
                
        else:
            secondterm = re.sub("%", '', te)
            searchdatabase(secondterm,cursor,termsDB) #should call the iterating function
    
            
    #NewSearch = input("Do you want to start a new search?(y/n) ")
    #if(NewSearch == "y"): #Termination Condition
    #main()   
                
    
    #cursor.close()
    #termsDB.close()    
    
def pricefunct(pr):
    #print(pr)
    priceDB = db.DB()
    priceDB.open('pr.idx',None,db.DB_BTREE,db.DB_CREATE)   
    price1 = re.compile("price\>[0-9]")
    price2 = re.compile("price\<[0-9]")
    price3 = re.compile("price\=[0-9]")
    cursor = priceDB.cursor()
    if pr != 0: 
        if (price1.match(pr))and (price2.match(pr)):
            greatpr=re.sub("price\>",'',pr)
            tab = 20 - len(greatpr)
            n =(tab*' ') + greatpr
            greatpr = n            
            lesspr=re.sub("price\<",'',pr)
            tab1 = 20 - len(lesspr)
            n1 =(tab1*' ') + lesspr 
            lesspr = n1            
        elif (price2.match(pr))and not (price1.match(pr)):
            lesspr=re.sub("price\<",'',pr)
            tab1 = 20 - len(lesspr)
            n1 =(tab1*' ') + lesspr 
            lesspr = n1            
            greatpr = None
        elif (price1.match(pr)) and not (price2.match(pr)):
            greatpr=re.sub("price\>",'',pr)
            tab = 20 - len(greatpr)
            n =(tab*' ') + greatpr
            greatpr = n            
            lesspr = None                       
         
        if (price3.match(pr)):
            money1 = re.sub("price\=",'',pr)
            tab = 20 - len(money1)
            m =(tab*' ') + money1
            money = m            
            searchdatabase(money,cursor, priceDB)
        else:  
            rangesearch(greatpr, lesspr, cursor, priceDB)#commented out the range function       
            
def date_cat_loc(da,ca,lo):
    date1 = re.compile("date\>\\d{4}\/\d{2}\/\d{2}")
    date2 = re.compile("date\<\\d{4}\/\d{2}\/\d{2}")
    category= re.compile("cat\=[A-Za-z_-]")
    location = re.compile("location\=[A-Za-z0-9]")  
    adDB = db.DB()
    adDB.open('ad.idx',None,db.DB_HASH,db.DB_CREATE)
    cursor = adDB.cursor()
    
    if lo != 0: 
        loc = re.sub('location\=','', lo)
        record = cursor.first()
    while (record != None):
        ad = str(record[1].decode("utf-8"))
        if ad == None:
            break
        findloc = re.search('<loc>(.*)</loc>',ad)
        location  = findloc.group(1)
        if (loc == location):
            found = (str(record[0].decode("utf-8")) + ": " + str(record[1].decode("utf-8")))
            resultlist.add(found)
        record = cursor.next()
#getquery()
   
    if da != 0:  
        if (date1.match(da)):
            greatda=re.sub('date\>','',da)
           # print("great date",greatda)
        if (date2.match(da)):
            lessda=re.sub('date\<','',da)
         #   print("less date",lessda)
    else: 
        greatda = None
        lessda = None        
    #rangesearch(greatda, lessda, cursor, pdateDB)
        
    if ca != 0: 
        if(category.match(ca)):
            cat = re.sub('cat\=','',ca)
           # print('category',cat)
    else: 
        ca = None       
    #cursor = pdatesDB.cursor()
    #searchdatabase(ca,cursor, pdatesDB)  
    
def rangesearch(n, n1, cursor, database): 

    global resultlist
    if n ==  None:
        n = cursor.first()
        n = (n[0].decode("utf-8"))
    if n1 == None:
        n1 = cursor.last()
        n1 = (n1[0].decode("utf-8")) 
    
    #while(True):
    result = cursor.set_range(n.encode("utf-8")) 
    
    if(result != None):
        #print("List of found descriptions:")
    
        while(result != None):
            #Checking the end condition: If the student's name comes after(or equal to) Ending_Name
            if(str(result[0].decode("utf-8")[0:len(n1)])>=n1): 
                break
            
            ans = (str(result[0].decode("utf-8")) + ": " + str(result[1].decode("utf-8")))
            #print(ans)            
            resultlist.add(ans)
            result = cursor.next() 
            #print(resultlist)
    else:
        print("No ranges were found")
        #main()    
        NewSearch = input("Do you want to start a new search?(y/n) ")
        if(NewSearch != "y"): #Termination Condition
            main()
        #else:
            

def searchdatabase(name,cursor,database):
    global resultlist
    result = cursor.set(name.encode("utf-8")) 
    #In the presence of duplicate key values, result will be set on the first data item for the given key. 

    if(result != None):
        #print("List of descriptions that match:")
        ans3 = (str(result[0].decode("utf-8")) + " : " + str(result[1].decode("utf-8")))
        resultlist.add(ans3)
        
        #iterating through duplicates:
        dup = cursor.next_dup()
        while(dup != None):
            ans33 = (str(dup[0].decode("utf-8")) + " : " + str(dup[1].decode("utf-8")))
            #print(ans33)            
            resultlist.add(ans33)
            dup = cursor.next_dup()
    #else:
        #print("No Entry Found.")
        #NewSearch2 = input("Do you want to start a new search?(press y/n) ")
        #if(NewSearch2 != "y"): #Termination Condition
          #  sys.exit()
        #else:
        #main() 
            
def getquery():
    global resultlist
    
    templist = list(resultlist)
    adDB = db.DB()
    adDB.open('ad.idx',None,db.DB_HASH,db.DB_CREATE)
    cursor = adDB.cursor()   
    
    final = []
    firstlist = []
    aids = []
    ylist = []
    output = input("Please specify your output(full/brief):" )
    #"output=full" "output=brief".
        
    for i in resultlist:
        n = i.split(':')
        firstlist.append(n)
    #print('fisrt:',firstlist)
        
    if firstlist == []:
        print('No records found')
    
    
    for i in range (len(firstlist)):
        Ads = firstlist[i][1]       
        splitAds = Ads.split(',')
        Ads = splitAds[0]
        Ads = Ads[:-1]
        if Ads:    
            aids.append(Ads)
    
    print()
    for y in aids:
        if output == "full":
            ylist.append(y)

            full = adDB.get(y.encode('utf-8'))
            
            #full=str(full.decode('utf-8'))
            #print('full', full)
            
            if full != None:
                final.append(str(full))
                #print('Full list = ',final)    
                print()       
            else:
                print('full none')
        
        elif output == "brief":
            term = cursor.set(y.encode("utf-8"))
            if(term != None):
                ad = str(term[1].decode("utf-8"))
                getphrase = re.search('<ti>(.*)</ti>',ad)
                phrase = getphrase.group(1)
                print(str(term[0].decode("utf-8")) + ": " + phrase)
            
        else:
            print('Enter a valid option')

    print('y',ylist)    
    
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

                    line = datesub(line)
        

                    list3.add(line)
                else:
                    list3.add(i[1])
        elif(date2.match(i) or date4.match(i)):
            idealdate2.append(i)
            for i in idealdate2:
                i = i.split("<")
                dlequal = re.compile("=\\d{4}\/\d{2}\/\d{2}")

                if(dlequal.match(i[1])):

                    line = re.sub('=', '', i[1])

                    line = dateadd(line)
                    #print("end",dateadd)

                    list4.add(line)
                else:
                    list4.add(i[1])        

        else:
            finallist.add(i)  



    list1= list(list1)   



    if list1 != []:        
        m = max(list1) 

        for i in idealprice1:
            if "price>"+str(m)==i :   
                finallist.add(i)  
            elif "price>="+ str(m+1)==i :
                finallist.add("price>" +str(m))


    list2 = list(list2)      
    if list2!= []:
        n = min(list2)

        for j in idealprice2:
            if "price<"+str(n)==j : 
                finallist.add(j)
            elif "price<="+ str(n-1)==j :
                finallist.add("price<"+str(n))

    list3 = list(list3)
    

    if list3!= []:
        k = mindate(list3)


        for j in idealdate1:
            
            if "date>"+str(k)==j: 
                finallist.add(j)
            elif "date>="+ dateadd(k)==j :
                
                finallist.add("date>" + str(k))

    list4 = list(list4) 
    

    if list4!= []:
        k = maxdate(list4)


        for j in idealdate2:
            if "date<"+str(k)==j : 
                finallist.add(j)
            elif "date<="+ datesub(k)==j :
               
                finallist.add("date<"+str(k)) 

    finallist = list(finallist) 

    return finallist

def main():
    print("Please enter your query, type exit to quit.")
    #while True:
    text = input()
    text = text.strip(" ")
    text = " "+text 
    #if text == "exit":
      #  break
        #else:
            #print(getidealcond(text))
            #break             
    fetch(text)
    getquery()

if __name__ == "__main__":
        main()
        
