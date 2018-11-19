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
                aid = ad[2][0:10]
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
                    word = '&#'
                    #-------------------------------------------                                      
                    result = (re.search(r'(\w+)\.{3,}', i)) 
                    if result == None:
                        for c in word:
                            if c in i:
                                regex1 = re.sub('[^A-Za-z\\_\\-]+','', i) 
                            else:             
                                regex1 = re.sub('[^A-Za-z0-9\\_\\-]+','', i)
                        if len(regex1) > 2:
                            regex1 = regex1.lower()
                            
                            a = regex1 + ":"
                            info = a+ aid 
                            terms.write(str(info)+  "\n")                        
                    else:                                                             
                        res = re.split("\.+", i)                        
                        for y in res:
                            for c in word:
                                if c in y:
                                    regex1 = re.sub('[^A-Za-z\\_\\-]+','', y) 
                                else:             
                                    regex1 = re.sub('[^A-Za-z0-9\\_\\-]+','', y)
                                    
                            if len(regex1) > 2:
                                regex1 = regex1.lower()
                                
                                a = regex1 + ":"
                                info = a+ aid 
                                terms.write(str(info)+  "\n")                            
                         #--------------------------------------       
                   
                    
                    
                desc = ad[12][:-6]
                desc = desc.split(" ")            
                for k in desc:
                    word = '&#'
                    #------------------------------------                   
                    result1 = (re.search(r'(\w+)\.{3,}', k)) 
                    if result1 == None:
                        for b in word:
                            if b in k:                    
                                regex2 = re.sub('[^A-Za-z\\_\\-]+','', k)
                            else:
                                regex2 = re.sub('[^A-Za-z0-9\\_\\-]+','', k)
                                
                        if len(regex2) > 2:
                            regex2 = regex2.lower()
                            
                            t = regex2 + ":"
                            info2 = t + aid 
                            terms.write(str(info2)+  "\n")                        
                    else:                        
                        res1 = re.split("\.+", k)
                        for y1 in res1:                           
                            for c in word:
                                if c in y1:
                                    regex2 = re.sub('[^A-Za-z\\_\\-]+','', y1) 
                                else:             
                                    regex2 = re.sub('[^A-Za-z0-9\\_\\-]+','', y1) 
                                
                            if len(regex2) > 2:
                                regex2 = regex2.lower()
                                
                                t = regex2 + ":"
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
    # hash index for the terms
    cmd = "sort<terms.txt -u > terms2.txt"
    subprocess.call(cmd, shell=True)    
    
    # B+ index for the prices
    cmd = "sort<prices.txt  > price2.txt"
    subprocess.call(cmd, shell=True)          

    #B+ index for the pdates
    cmd = "sort<pdates.txt  > pdates2.txt"
    subprocess.call(cmd, shell=True) 
    
    #B+ index for the ads
    cmd = "sort<ads.txt  > ads2.txt"
    subprocess.call(cmd, shell=True)
    
def main():
    phase1()
    phase2()

if __name__ == "__main__":
    main()
    
      
