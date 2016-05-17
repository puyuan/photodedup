import os
import re
f=open("../data/filelist_sort_by_size", "r")

filecount={}

for line in f:
        match=re.search(r'\d{4}:\d{2}:\d{2}\s+\d{2}:\d{2}:\d{2}', line)
        if(match==None):
            continue
        datetime=match.group(0)
        if (not filecount.has_key(datetime)):
            filecount[datetime]=0
        filecount[datetime]+=1

#for k, v in filecount.items(): 
#	print k, v


f=open("../data/filelist_sort_by_size", "r")
for line in f:
	arr=line.split(",")
	if len(arr)<2:
		continue
	file_path=arr[0]
	datetime=arr[1].strip()
	if(filecount.has_key(datetime) and filecount[datetime]>1):
		print file_path
		try:
                        print "removing image: %s"%(file_path)
			os.remove(file_path)
		except:
			print "file doesn't exist, perhaps deleted already?"
		filecount[datetime]-=1
	
	
