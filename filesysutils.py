import os
import sys
def format_bytes(size):
    # 2**10 = 1024
    power = 2**10
    n = 0
    power_labels = {0 : '', 1: 'kilo', 2: 'mega', 3: 'giga', 4: 'tera'}
    while size > power:
        size /= power
        n += 1
    return size, power_labels[n]+'bytes'

def dupefiles(rootdir, searchstring=".", sizethreshold=0):
    """ Find duplicate files in the rootdir matching the given searchstring with total size larger than the sizethreshold  """
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
                pthname = "\\\\?\\" + os.path.join(root, name)
                try:
                    filedict[pthname] = os.stat(pthname).st_size
                except:
                    filedict[pthname] = 0
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
                pthname =  "\\\\?\\" + os.path.join(root, name)
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
    ''' list files in the directory, recursively or non-recursively'''
    if recursive:
        for root, dir, files in os.walk(rootdir):
            for name in files:
                print(name) 
    else:
        for f in os.listdir(rootdir):
            if os.path.isfile(os.path.join(rootdir,f)):
                print(f)

def search(rootdir, searchstring="*", min_size=0, max_size =32e9, startdate = "1970-01-01", stopdate = "2100-12-31" ):
    '''
    Prints the paths of the file search results.

            Parameters:
                    rootdir(string) : The root directory to start search
                    searchstring (string): Optional, default "*". search string in UNIX style file search using wildcards "*" for 0 or more characters, ? for exactly one character.
                    minsize (integer): Optional, default 0. The minimum file size for search.
                    maxsize (integer): Optional, default 32e9 or 32 GB. The maximum file size for search.
                    startdate (string): Optional, default "1970-01-01". The earliest modified date.
                    stopdate (string): Optional, default "2100-12-31". The latest modified date.

            Returns:
                    None
    '''
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
                fileinfo = os.stat("\\\\?\\" + fullpath)
                mdate = datetime.datetime.fromtimestamp(fileinfo.st_mtime).date()
                if ((os.stat(fullpath).st_size) >= min_size and 
                        (os.stat(fullpath).st_size) <=max_size and 
                        mdate >= startdate and 
                        mdate <= stopdate):
                    sz, lbl = format_bytes(fileinfo.st_size)
                    print(fullpath," | ",str(round(sz))+" "+lbl, " | ", mdate)
            except:
                print("*ERROR in: " + fullpath)
                pass

def search_user():
    '''thin wrapper function for the search with minimal error handling '''
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
    
def search_contents(rootdir, fileext="txt", text_to_search=""):
    ''' search with contents of text or text like files '''
    for root, dir, files in os.walk(rootdir):
        for name in files:
            if "."+fileext in name:
                with open(os.path.join(root,name),errors='ignore') as f:
                    textdata = f.read()
                    if text_to_search in textdata:
                        print(os.path.join(root,name)) 
    
    pass



#driver code
if __name__ == "__main__":
    #dupefiles("F:", ".",10_000_000)
    #findlargest("F:", 30, searchstring=".")
    #finduniques("D:\\Dropbox\\Reading material", "D:\\Dropbox\epubs")
    #findoldest("D:\\Dropbox", 30, searchstring=".")
    #listfiles("D:\\Desktop", recursive=0)
    #search("E:\\Laptop fullbkpup", "*vaibhav*.jpg*") #, startdate = "2017-06-01", stopdate= " 2017-07-31")
    #search_user()
    #search_contents("d:\\desktop", fileext="py")

    print("What do you want to do?")
    print("1:" + dupefiles.__doc__ + "?")
    print("2:" + findlargest.__doc__ + "?")
    print("3:" + finduniques.__doc__ + "?")
    print("4:" + findoldest.__doc__ + "?")
    print("5:" + listfiles.__doc__ + "?")
    print("6:" + " Search for files in rootdir based on searchstring in UNIX style file search using wildcards , minsize, maxsize, startdate,stopdate" + "?")
    print("7:" + search_contents.__doc__ + "?")
    choice = input("Enter your choice from 1 to 7: ")
    
    if choice == "1":
        rootdir = input("Enter full path: ")
        if rootdir == '':
            print("Path is mandatory")
            sys.exit()

        n = input ("size threshold: ")
        n = 0 if (n == '') else int(n)
        
        searchstring = input("Enter Searchstring (Press enter to leave unspecified): ")
        searchstring = "." if (searchstring == '') else searchstring

        dupefiles(rootdir, searchstring, n)

    elif choice == "2":
        #rootdir, n, searchstring=""
        rootdir = input("Enter full path: ")
        if rootdir == '':
            print("Path is mandatory")
            sys.exit()
        
        n = input ("number of results: ")
        n = 10 if (n == '') else int(n)
        
        searchstring = input("Enter Searchstring (Press enter to leave unspecified): ")
        searchstring = "" if (searchstring == '') else searchstring

        findlargest(rootdir, n, searchstring)

    elif choice == "3":
        rootdir1 = input("Enter full path: ")
        if rootdir1 == '':
            print("Path is mandatory")
            sys.exit()

        rootdir2 = input("Enter full path: ")
        if rootdir2 == '':
            print("Path is mandatory")
            sys.exit()
        finduniques(rootdir1, rootdir2)

    elif choice == "4":
        rootdir = input("Enter full path: ")
        if rootdir == '':
            print("Path is mandatory")
            sys.exit()
        n = input ("number of results: ")
        n = 10 if (n == '') else int(n)
        
        searchstring = input("Enter Searchstring (Press enter to leave unspecified): ")
        searchstring = "" if (searchstring == '') else searchstring

        findoldest(rootdir, n, searchstring)

    elif choice == "5":
        rootdir = input("Enter full path: ")
        if rootdir == '':
            print("Path is mandatory")
            sys.exit()
        
        recursive = (input("recursive? 0 for no and 1 for yes"))
        nrecursive= 0 if (recursive == '') else 1

        listfiles(rootdir, recursive)

    elif choice == "6":
        search_user()
    
    elif choice == "7":
        rootdir = input("Enter full path: ")
        if rootdir == '':
            print("Path is mandatory")
            sys.exit()
        fileext = input("Enter fileext (Press enter to leave unspecified): ")
        fileext = "txt" if (searchstring == '') else searchstring

        text_to_search = input("Enter text_to_search (Press enter to leave unspecified): ")
        text_to_search = "" if (text_to_search == '') else text_to_search
        
        search_contents(rootdir, fileext, text_to_search)

    else:
        print("wrong choice, rerun the program and try again")



