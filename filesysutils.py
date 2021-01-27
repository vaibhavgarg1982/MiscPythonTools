import os
#import matplotlib.pyplot as plt
def format_bytes(size):
    # 2**10 = 1024
    power = 2**10
    n = 0
    power_labels = {0 : '', 1: 'kilo', 2: 'mega', 3: 'giga', 4: 'tera'}
    while size > power:
        size /= power
        n += 1
    return size, power_labels[n]+'bytes'

def dupefiles(rootdir, searchstring, sizethreshold=0):
    """ function to find duplicate files in the rootdir matching the given searchstring with total size larger than the sizethreshold  """
    filedict={}
    
    #populate the dictionary
    for root, dir, files in os.walk(rootdir):
        for name in files:
            filedict.setdefault(name,[]).append(os.path.join(root, name))
            #print(os.path.join(root, name))
    
    
    for entry in filedict: # filename as key, list of paths as value
        nument=len(filedict[entry])
        if nument > 1 and entry.find(searchstring)!=-1:
            #print(entry)
            totsize = 0
            for pathstring in filedict[entry]:
                totsize = totsize+os.stat(pathstring).st_size

            if totsize >= sizethreshold:
                print(entry)
                for pathstring in filedict[entry]:
                    print(f"{pathstring} size:{int(os.stat(pathstring).st_size/1024)}KB")
                print()
    pass

def findlargest(rootdir, n, searchstring=""):
    """ find n largest files in the root dir matching the searchstring. Leave out searchstring for all files """
    filedict={}
    i = 0
    for root, dir, files in os.walk(rootdir):
        for name in files:
            if name.find(searchstring)!=-1:
                pthname = os.path.join(root, name)
                filedict[pthname] = os.stat(pthname).st_size
                i+=1
                if i>100:
                    print(".", end="")
                    i=0
                #print(pthname)
    
    output = (sorted(filedict, key= filedict.get, reverse = True)[0:n])
    print()

    for pth in output:
        print(f"{pth}---{int(filedict[pth]/(1024*1024)+0.5)} MB")

def finduniques(rootdir1, rootdir2):
    """ find files in rootdir 1 that are not in rootdir 2 """
    lstrootdir1=[]
    lstrootdir2=[]
    for root, dir, files in os.walk(rootdir1):
        for name in files:
            lstrootdir1.append((name, os.stat(os.path.join(root, name)).st_size))
    
    for root, dir, files in os.walk(rootdir2):
        for name in files:
            lstrootdir2.append((name, os.stat(os.path.join(root, name)).st_size))
    
    for flname in lstrootdir1:
        if flname not in lstrootdir2:
            print(flname)
    pass

def findoldest(rootdir, n, searchstring=""):
    """ find n oldest files in the root dir matching the searchstring. Leave out searchstring for all files """
    import datetime
    filedict={}
    i = 0
    for root, dir, files in os.walk(rootdir):
        for name in files:
            if name.find(searchstring)!=-1:
                pthname = os.path.join(root, name)
                filedict[pthname] = os.stat(pthname).st_atime
                i+=1
                if i>100:
                    print(".", end="")
                    i=0
                #print(pthname)
    
    output = (sorted(filedict, key= filedict.get)[0:n])
    print()

    for pth in output:
        print(f"{pth}---last acccessed in: {datetime.datetime.fromtimestamp(filedict[pth]).year} ")
        
def listfiles(rootdir, recursive=0):
    
    if recursive:
        for root, dir, files in os.walk(rootdir):
            for name in files:
                print(name) 
    else:
        for f in os.listdir(rootdir):
            if os.path.isfile(os.path.join(rootdir,f)):
                print(f)

def search(rootdir, searchstring="*", min_size=0, max_size =32e9, startdate = "1970-01-01", stopdate = "2100-12-31" ):
    import fnmatch, datetime
    filedict={}
    startyear, startmonth, startdate = map(int, startdate.split("-"))
    startdate = datetime.date(startyear, startmonth, startdate)
    stopyear, stopmonth, stopdate = map(int, stopdate.split("-"))
    stopdate = datetime.date(stopyear, stopmonth, stopdate)
    #populate the dictionary
    for root, dir, files in os.walk(rootdir):
        for name in files:
            filedict.setdefault(name,[]).append(os.path.join(root, name))
    #res = {dct:filedict[dct] for dct in filedict if searchstring in dct}
    res = {dct:filedict[dct] for dct in filedict if 
                                fnmatch.fnmatch(dct, searchstring)}
    
    for k in res:
        for fullpath in res[k]:
            try:
                fileinfo = os.stat(fullpath)
                mdate = datetime.datetime.fromtimestamp(fileinfo.st_mtime).date()
                if ((os.stat(fullpath).st_size) >= min_size and 
                        (os.stat(fullpath).st_size) <=max_size and 
                        mdate >= startdate and 
                        mdate <= stopdate):
                    sz, lbl = format_bytes(fileinfo.st_size)
                    print(fullpath," | ",str(round(sz))+" "+lbl, " | ", mdate)
            except:
                pass

def search_user():
    '''wrapper function for the search with minimal error handling '''
    rootdir = input("Enter full path: ")
    if rootdir == '':
        print("Path is mandatory")
        return
    
    searchstring = input("Enter Searchstring with wildcards (Press enter to leave unspecified): ")
    searchstring = "*" if (searchstring == '') else searchstring

    min_size = input ("minsize (Press enter to leave unspecified): ")
    min_size = 0 if (min_size == '') else int(min_size)

    max_size = input ("maxsize (Press enter to leave unspecified): ")
    max_size = 32e9 if (max_size == '') else int(max_size)

    startdate = input("Enter startdate in yyyy-mm-dd format (Press enter to leave unspecified): ")
    startdate = "1970-01-01" if (startdate == '') else startdate

    stopdate = input("Enter stopdate in yyyy-mm-dd format (Press enter to leave unspecified): ")
    stopdate = "2100-12-31" if (stopdate == '') else stopdate

    print(f"searching with {rootdir=}, {searchstring=}, {min_size=}, {max_size=}, {startdate=} , {stopdate=}")
    search(rootdir, searchstring, min_size, max_size, startdate , stopdate )
    




#driver code
if __name__ == "__main__":
    #dupefiles("F:", ".",10_000_000)
    #findlargest("F:", 30, searchstring=".")
    #finduniques("D:\\Dropbox\\Reading material", "D:\\Dropbox\epubs")
    #findoldest("D:\\Dropbox", 30, searchstring=".")
    #listfiles("D:\\Desktop", recursive=0)
    #search("E:\\Laptop fullbkpup", "*vaibhav*.jpg*") #, startdate = "2017-06-01", stopdate= " 2017-07-31")
    search_user()



    pass

