import os

filelist = os.listdir("testdir")
 
for file in filelist:
    if os.path.isfile(os.path.join("testdir",file)):
        year = int(file[0:4])
        month = int(file[4:6])
        date = int(file[6:8])
        if month == 0 or date ==0 :
            print("stop")
        os.makedirs(os.path.join("testdir", format(year),(format(month,"02")),(format(date, "02"))), exist_ok = True)
        dest = (os.path.join("testdir", format(year),(format(month,"02")),(format(date, "02")), file))
        src = os.path.join("testdir", file)
        os.replace(src, dest)
        print(f"{file}: {dest=} from {src=}")
 
