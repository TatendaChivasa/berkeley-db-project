from bsddb3 import db
DB_ad = "ad.idx"
DB_te = "te.idx"
DB_da = "da.idx"
DB_pr = "pr.idx"

database = db.DB()
database.set_flags(db.DB_DUP) #declare duplicates allowed before you create the database
#database.open(DB_ad,None, db.DB_HASH)
#database.open(DB_te,None, db.DB_BTREE)
#database.open(DB_da,None, db.DB_BTREE)
database.open(DB_pr,None, db.DB_BTREE)

curs = database.cursor()

while(True):
    name = input("Enter a Name to look up: ")
    if(name == "q"): #Termination Condition
        break
    
    result = curs.set(name.encode("utf-8")) 
    #In the presence of duplicate key values, result will be set on the first data item for the given key. 
   
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
database.close()
