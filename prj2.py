from bsddb3 import db
import sys 
import re
import subprocess

def phase1():
    pdates = open("pdates.txt", 'w')
    ads = open("ads.txt", 'w')
    terms = open("terms.txt", 'w')
    prices = open("prices.txt", 'w')
    
    filein =  open(sys.argv[1], 'r')
    
    if sys.argv[1] is None:
        print("Invalid file argument")    
    else:
        for line in filein:
            
            ad = line.split(">")
            
            if ad[0] == '<ad':  
                aid = ad[2][0:-5]
            # the ads file formats
                expr = aid + ':' 
                ads.write(expr + line+ " ")
    
                
                category = ad[8][:-5]
                city = ad[6][:-5]
                
                prizes = ad[14][:-7]
                prizes = prizes.split(" ")
                
                title = ad[10][:-4]
                title = title.split(" ")
                
                datte = ad[4][:-6]
                datte = datte.split(" ")
                
        #the term file format
                for i in title:
                    regex1 = re.sub('&#\d\d\d;','',i)
                    regex1 = re.sub('[^A-Za-z0-9\\_\\-]',' ', regex1)                                                        
                    if len(regex1) > 2:
                        if (' ' in  regex1):
                            regex1 = regex1.split(' ')
                            for reg in regex1:
                                if len(reg) > 2:
                                    reg = reg.lower()                          
                                    t = reg + ":"
                                    info = t + aid 
                                    terms.write(str(info)+  "\n")                        
                        else:
                            regex1 = regex1.lower()                          
                            t = regex1 + ":"
                            info = t + aid 
                            terms.write(str(info)+  "\n")                                              
                         #--------------------------------------       
                   
                    
                    
                desc = ad[12][:-6]
                desc = desc.split(" ")            
                for k in desc:                   
                    regex2 = re.sub('&#\d\d\d;','',k)
                    regex2 = re.sub('[^A-Za-z0-9\\_\\-]',' ', regex2) 
                    if len(regex2) > 2:
                        if (' ' not in regex2):
                            regex2 = regex2.lower()                          
                            t = regex2 + ":"
                            info2 = t + aid 
                            terms.write(str(info2)+  "\n")                             
                                                 
                        else:                                                    
                            regex2 = regex2.split(' ')
                            for reg1 in regex2:
                                if len(reg1) > 2:
                                    reg1 = reg1.lower()                          
                                    t = reg1 + ":"
                                    info2 = t + aid 
                                    terms.write(str(info2)+  "\n")                               
                    #-----------------------------------------------
                    
                        
        # the pdates file format
                for p in datte:
                    
                    if len(p) > 2:
                        p = p.lower()
                        rest = aid + ',' + category + ',' + city
                        j = p + ":"
                        info4 = j + rest            
                        pdates.write(str(info4) + "\n")
                        
        
                for n in prizes:
                    n = n.lower()
                    rest = aid + ',' + category + ',' + city
                    q = n + ":"
                    info3 = q + rest            
                    prices.write( str(info3)+ "\n")
                
    terms.close()
    prices.close()
    pdates.close()
    ads.close()
    
def phase2():  
    # B+ index for the terms
    DB_File = "te.idx"
    database = db.DB()
    #database.set_flags(db.DB_DUP) 
    database.open(DB_File,None, db.DB_BTREE, db.DB_CREATE)
    curs = database.cursor()
    cmd = "sort<terms.txt -u > terms2.txt"
    subprocess.call(cmd, shell=True) 
    
    term = open("terms2.txt", 'r')
    listterms = []
    for i in term:
        ad = i.split(":")  
        listterms.append(ad)    
    for t in range(len(listterms)):
        tkey = listterms[t][0]
        tval = listterms[t][1]
        t += 1
        
        database.put(bytes(tkey, "utf 8"), bytes(tval, "utf-8"))
    curs.close()
    database.close()    
   
    # B+ index for the prices
    DB_File = "pr.idx"
    database = db.DB()
    database.set_flags(db.DB_DUP) 
    database.open(DB_File,None, db.DB_BTREE, db.DB_CREATE)
    curs = database.cursor()
    cmd1 = "sort<prices.txt  > price2.txt"
    subprocess.call(cmd1, shell=True)          

    price = open("price2.txt", 'r')
    plistt = []
    for i in price:
        ad1 = i.split(":")  
        plistt.append(ad1)    
    for k in range(len(plistt)):
        kkey = plistt[k][0]
        kval = plistt[k][1]
        k += 1
        
        database.put(bytes(kkey, "utf 8"), bytes(kval, "utf-8"))
    curs.close()
    database.close()    
    
    #B+ index for the pdates
    DB_File = "da.idx"
    database = db.DB()
    database.set_flags(db.DB_DUP) 
    database.open(DB_File,None, db.DB_BTREE, db.DB_CREATE)  
    curs = database.cursor()
    cmd2 = "sort<pdates.txt  > pdates2.txt"
    subprocess.call(cmd2, shell=True) 
    
    pdate = open("pdates2.txt", 'r')
    datelist = []
    for i in pdate:
        ad2 = i.split(":")  
        datelist.append(ad2)    
    for p in range(len(datelist)):
        pkey = datelist[p][0]
        pval = datelist[p][1]
        p += 1
        
        database.put(bytes(pkey, "utf 8"), bytes(pval, "utf-8"))
    curs.close()
    database.close()       
    
    #hash index for the ads
    DB_File = "ad.idx"
    database = db.DB()
    #database.set_flags(db.DB_DUP)
    database.open(DB_File,None, db.DB_HASH, db.DB_CREATE)       
    cmd3 = "sort<ads.txt  > ads2.txt"
    subprocess.call(cmd3, shell=True)
    
    ads = open("ads2.txt", 'r')
    adlist = []
    for i in ads:
        ad3 = i.split(":")  
        adlist.append(ad3) 
    #print(adlist)
    
    for m in range(1, (len(adlist))):
        mkey = adlist[m][0]
        mval = adlist[m][1]
        m += 1  
        
        database.put(bytes(mkey, "utf 8"), bytes(mval, "utf-8"))
    curs.close()
    database.close()  
    
def phase3():
    
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
     
def main():
    phase1()
    phase2()
    #phase3()

if __name__ == "__main__":
    main()
    
      