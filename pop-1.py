from bsddb3 import db

adsDB = db.DB()
termsDB = db.DB()
pdatesDB = db.DB()
priceDB = db.DB()
adsDB.open('ad.idx',None,db.DB_HASH,db.DB_CREATE)
termsDB.open('te.idx',None,db.DB_BTREE,db.DB_CREATE)
pdatesDB.open('da.idx',None,db.DB_BTREE,db.DB_CREATE)
priceDB.open('pr.idx',None,db.DB_BTREE,db.DB_CREATE)
    

curs = pdatesDB.cursor()

while(True):
    name = input("Enter a Name to look up: ")
    if(name == "q"): #Termination Condition
        break
    
    result = curs.set(name.encode("utf-8")) 
    #In the presence of duplicate key values, result will be set on the first data item for the given key. 
   
    if(result != None):
        print("List of descriptionns that match:")
        print("Key: " + str(result[0].decode("utf-8")) + ", Value: " + str(result[1].decode("utf-8")))
        
        #iterating through duplicates:
        dup = curs.next_dup()
        while(dup != None):
            print("key: " + str(dup[0].decode("utf-8")) + ", Value: " + str(dup[1].decode("utf-8")))
            dup = curs.next_dup()
    else:
        print("No Entry Found.")
            

curs.close()
priceDB.close()