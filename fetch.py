def fetch():
    
    querylist = ['date<=2018/11/07','date>=2018/11/05','price > 20', 'price < 40',' location = edmonton','cat=art-collectibles','camera']
    
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
        #curs = priceDB.cursor()
        print('pr')
        print(pr)
    
def date(da):
    if len(da) != 0: 
        #curs = pdatesDB.cursor()
        print('da')
        print(da)
        
def location(lo):
    if len(lo) != 0: 
        #curs = pricesDB.cursor()
        print('lo')
        print(lo)
        
def cat(ca):
    if len(ca) != 0: 
        #curs = pdatesDB.cursor()
        print('ca')
        print(ca)     

fetch()