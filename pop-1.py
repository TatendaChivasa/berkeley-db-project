from bsddb3 import db
import re

termsDB = db.DB()
termsDB.open('te.idx',None,db.DB_BTREE,db.DB_CREATE)
    
cursor = termsDB.cursor()

while(True):
    name = input("Enter a Name to look up: ")
    te = name
    if(name == "q"): #Termination Condition
        break 
    
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
                print("List of found descriptions:")
            
                while(result != None):
                    #Checking the end condition: If the student's name comes after(or equal to) Ending_Name
                    if(str(result[0].decode("utf-8")[:end])!=n): 
                        break
                    
                    print(str(result[0].decode("utf-8")) + ": " + str(result[1].decode("utf-8")))
                    result = cursor.next() 
            else:
                print("No ranges were found")
                
        else:
            secondterm = re.sub("%", '', te)
            
            #def searchdatabase(name,cursor,database) #shoul call the iterating function
    
            
    NewSearch = input("Do you want to start a new search?(press y for yes) ")
    if(NewSearch != "y"): #Termination Condition
        break    
            

cursor.close()
termsDB.close()