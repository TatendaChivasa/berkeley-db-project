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
                    abuni = re.sub('[^A-Za-z0-9\\_\\-]+','', i)
                    
                    if len(abuni) > 2:
                        abuni = abuni.lower()
                        
                        a = abuni + ":"
                        info = a+ aid 
                        terms.write(str(info)+  "\n")
                desc = ad[12][:-6]
                desc = desc.split(" ")            
                for k in desc:
                    tatenda = re.sub('[^A-Za-z0-9\\_\\-]+','', k)
                    if len(tatenda) > 2:
                        tatenda = tatenda.lower()
                        
                        t = tatenda + ":"
                        info2 = t + aid 
                        terms.write(str(info2)+  "\n")
                        
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
    
      
