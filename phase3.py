from bsddb3 import db

def phase3():
    # commented out but will be ised for later query matching and selection
    """
    user = input("enter your query: ").lower().replace(" ", "")
    #print(user)

    #start_date_equal = re.match("date=", user) 
    #if start_date_equal != None:
    for x2 in re.finditer('date=', user):
        #print(start_date_equal)
        print(x2.start(), x2.end(), x2.group())  
    #end_date_equal = user.find("date") or user.find("price") or user.find("location") or 21 
    #end_date_equal = start_date_equal + 16
    #date_equal = user[start_date_equal : end_date_equal]
    
    
    start_date_greater = re.match("date>", user)
    if start_date_greater != None:
        print(start_date_greater)
    #end_date_greater = start_date_greater + 16
    #date_greater = user[start_date_greater : end_date_greater]
    
    
    #if user.find("date>=") and len == 6
    #start_date_greater_or_equal = re.match("date>=", user)
    for x1 in re.finditer('date>=', user):
    #if start_date_greater_or_equal != None:
        print(start_date_greater_or_equal)
    #end_date_greater_or_equal = start_date_greater_or_equal + 16
    #date_greater_or_equal = user[start_date_greater_or_equal : end_date_greater_or_equal]
    
    start_date_less = re.match("date<", user)
    if start_date_less != None:
        print(start_date_less)
    # = start_date_less + 16
    #date_less = user[start_date_less : end_date_less] 
    

    start_date_less_or_equal = re.match("date<=", user)
    if start_date_less_or_equal != None:
        print(start_date_less_or_equal)
    #end_date_less_or_equal = start_date_less_or_equal + 16
    #date_less_or_equal = user[start_date_less_or_equal : end_date_less_or_equal] 
    
    
    #start_price_equal = re.match("price=", user)
    #if start_price_equal != None:
        #print(start_price_equal)
        
    for x in re.finditer('price=', user):
        print(x.start(), x.end(), x.group())        
    #end_price_equal = start_price_equal + 8
    #price_equal = user[start_price_equal : end_price_equal]
    
    
    
    for x1 in re.finditer('price>', user):
        print(x1.start(), x1.end(), x1.group())   
        #start_price_greater = re.match("price>", user)
    #if start_price_greater != None:
     #   print(start_price_greater)
    #end_price_greater = start_price_greater + 8
    #price_greater = user[start_price_greater : end_price_greater]
    
    
    for x2 in re.finditer('price>=', user):
        print(x2.start(), x2.end(), x2.group())       
    #start_price_greater_or_equal = re.match("price>=", user)
    #if start_price_greater_or_equal != None:
     #   print(start_price_greater_or_equal)
    #end_price_greater_or_equal = start_price_greater_or_equal + 9
    #price_greater_or_equal = user[start_price_greater_or_equal : end_price_greater_or_equal]  
    
    
    start_price_less = re.match("price<", user)
    if start_price_less != None:
        print(start_price_less)
    #end_price_less = start_price_less + 8
    #price_less = user[start_price_less : end_price_less]
    

    start_price_less_or_equal = re.match("price<=", user)
    if start_price_less_or_equal != None:
        print(start_price_less_or_equal)
    #end_price_less_or_equal = start_price_less_or_equal + 9
    #price_less_or_equal = user[start_price_less_or_equal : end_price_less_or_equal]
    

    #The user should be able to change the output format to full record by typing "output=full" and back to id and title only using "output=brief"
    
    #first query returns all records that have camera as a word in the title or description fields. 
    
    #The second query returns all records that have a term starting with camera% in the title or description fields
    
    #put the user input in a list and but list could get really long 
"""
    #connection to the different databases
    adsDB = db.DB()
    termsDB = db.DB()
    pdatesDB = db.DB()
    priceDB = db.DB()
    adsDB.open('ad.idx',None,db.DB_HASH,db.DB_CREATE)
    termsDB.open('te.idx',None,db.DB_BTREE,db.DB_CREATE)
    pdatesDB.open('da.idx',None,db.DB_BTREE,db.DB_CREATE)
    priceDB.open('pr.idx',None,db.DB_BTREE,db.DB_CREATE)
        
    #cursors need to  be defined for each database when we connect and pass a query after matching
    curs = priceDB.cursor()
    
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

def main():
    phase3()

if __name__ == "__main__":
    main()