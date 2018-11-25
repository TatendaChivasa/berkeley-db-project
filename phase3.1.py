from bsddb3 import db
import re

querylist =  []   
queryeraser =  []



def main():    
    print("Please enter your query, type exit to quit.") #secify output form 
    while True:
        text = input()
        text = text.strip(" ")
        text = " "+text 
        if text == "exit":
            break
        else:
            parseQuery(text)
            break
        
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
    print("QueryList")
    print(querylist)
    fetch()

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
   
        

def fetch():
    global  querylist
    pr = 'price'
    da = 'date'
    lo = 'location'
    ca = 'cat'
    
    for a in querylist:
        if a.startswith(pr):
            price_location(a,0)

    for b in querylist:
        if b.startswith(da):
            date_cat(b,0) 
            
    for c in querylist:
        if c.startswith(lo):
            price_location(0,c)
            
    for d in querylist:
        if d.startswith(ca):
            date_cat(0,d)

    
def price_location(pr,lo):
    priceDB = db.DB()
    priceDB.open('pr.idx',None,db.DB_BTREE,db.DB_CREATE)
    #price = priceDB.curosr()    
    
    if pr != 0: 
        cursor = priceDB.cursor()
        #searchdatabase(pr,cursor, priceDB)
        
    if lo != 0: 
        cursor = priceDB.cursor()
        #searchdatabase(lo,cursor, priceDB)
            
def date_cat(da,ca):
    pdatesDB = db.DB()
    pdatesDB.open('da.idx',None,db.DB_BTREE,db.DB_CREATE)
    #pdat = pdatesDB.cursor()    
    
    if da != 0: 
        cursor = pdatesDB.cursor()
        #searchdatabase(da,cursor, pdateDB)
        
    if ca != 0: 
        cursor = pdatesDB.cursor()
        #searchdatabase(ca,cursor, pdatesDB)      

'''        
def location(lo):
    if len(lo) != 0: 
        cursor = pricesDB.cursor()
        #searchdatabase(lo,cursor)
 
       
def cat(ca):
    if len(ca) != 0: 
        cursor = pdatesDB.cursor()
        #searchdatabase(ca,cursor)    
'''    
       
def searchdatabase(name,cursor,database):
    adsDB = db.DB()
    adsDB.open('ad.idx',None,db.DB_HASH,db.DB_CREATE)
    #ad = ads.cursor()
    
    termsDB = db.DB()
    termsDB.open('te.idx',None,db.DB_BTREE,db.DB_CREATE)
    #term = termsDB.cursor()
    
    
    search = cursor.first()
    while search:           
        result = cursor.set(name.encode("utf-8")) 
        #In the presence of duplicate key values, result will be set on the first data item for the given key. 
        
        if(result != None):
            print("List of descriptionns that match:")
            print("Key: " + str(result[0].decode("utf-8")) + ", Value: " + str(result[1].decode("utf-8")))
            
            #iterating through duplicates:
            dup = cursor.next_dup()
            while(dup != None):
                print("key: " + str(dup[0].decode("utf-8")) + ", Value: " + str(dup[1].decode("utf-8")))
                dup = cursor.next_dup()
        else:
            print("No Entry Found.")   
            break
        
    cursor.close()
    priceDB.close()

if __name__ == "__main__":
        main()