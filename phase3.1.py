from bsddb3 import db
import re

querylist =  []   
queryeraser =  []

adsDB = db.DB()
adsDB.open('ad.idx',None,db.DB_HASH,db.DB_CREATE)
#ad = ads.cursor()

termsDB = db.DB()
termsDB.open('te.idx',None,db.DB_BTREE,db.DB_CREATE)
#term = termsDB.cursor()

pdatesDB = db.DB()
pdatesDB.open('da.idx',None,db.DB_BTREE,db.DB_CREATE)
#pdat = pdatesDB.cursor()

priceDB = db.DB()
priceDB.open('pr.idx',None,db.DB_BTREE,db.DB_CREATE)
#price = priceDB.curosr()


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
            price(a)

    for b in querylist:
        if b.startswith(da):
            date(b) 
            
    for c in querylist:
        if c.startswith(lo):
            location(c)
            
    for d in querylist:
        if d.startswith(ca):
            cat(d)

    
def price(pr):
    if len(pr) != 0: 
        cursor = priceDB.cursor()
        searchdatabase(pr,cursor, priceDB)
        
def date(da):
    if len(da) != 0: 
        cursor = pdatesDB.cursor()
        searchdatabase(da,cursor,pdatesDB)
        
def location(lo):
    if len(lo) != 0: 
        cursor = pricesDB.cursor()
        searchdatabase(lo,cursor,pdatesDB)
        
def cat(ca):
    if len(ca) != 0: 
        cursor = pdatesDB.cursor()
        searchdatabase(ca,cursor,pdatesDB)    
        
def searchdatabase(name,cursor,database):
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
        
    #curs.close()
   # priceDB.close()

if __name__ == "__main__":
        main()
