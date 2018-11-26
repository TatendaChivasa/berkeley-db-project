def rangesearch():
    priceDB = db.DB()
    priceDB.open('pr.idx',None,db.DB_BTREE,db.DB_CREATE)  
    
   
    cursor = priceDB.cursor()
    #if database == priceDB:

    
    while(True):
        startingvalue = input("Enter the Starting_value: ")
        endvalue = input("Enter the Ending_value: ")
        
        tab = 20 - len(startingvalue)
        n =(tab*' ') + startingvalue
        
        tab1 = 20 - len(endvalue)
        n1 =(tab1*' ') + endvalue       
        
        if n ==  None:
            n = cursor.first()
        if n1 == None:
            n1 = cursor.last()
            
        if(endvalue == "q"): #Termination Condition
                break         
        
        #get the record that has the smallest key greater than or equal to the Starting Name:
        result = cursor.set_range(n.encode("utf-8")) 
       
        if(result != None):
            print("List of found descriptions:")
        
            while(result != None):
                #Checking the end condition: If the student's name comes after(or equal to) Ending_Name
                if(str(result[0].decode("utf-8")[0:len(n1)])>=n1): 
                    break
                
                print(str(result[0].decode("utf-8")) + ": " + str(result[1].decode("utf-8")))
                result = cursor.next() 
        else:
            print("No ranges were found")
                
        NewSearch = input("Do you want to start a new search?(press y for yes) ")
        if(NewSearch != "y"): #Termination Condition
            break
 
#def searchdatabase(name,cursor,database):
def searchdatabase():  
    #print(name)
    
    while (True): 
       # name = input("Enter a student Name to look up: ")
        #if(name == "q"): #Termination Condition
          #  break  
        
        result = cursor.set(name.encode("utf-8")) 
        #In the presence of duplicate key values, result will be set on the first data item for the given key. 
        
        if(result != None):
            print("List of descriptions that match:")
            print("Key: " + str(result[0].decode("utf-8")) + ", Value: " + str(result[1].decode("utf-8")))
            
            #iterating through duplicates:
            dup = cursor.next_dup()
            while(dup != None):
                print("key: " + str(dup[0].decode("utf-8")) + ", Value: " + str(dup[1].decode("utf-8")))
                dup = cursor.next_dup()
        else:
            print("No Entry Found.")   
