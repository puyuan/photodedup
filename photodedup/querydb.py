import sqlite3
import os
import json
import hashlib
from dateutil.parser import parse
from dateutil.relativedelta import *
from math import ceil
import re
def retrieveVal(dic, key):
	if(dic.has_key(key)):
		return dic[key]
	else:
		return "" 

def week_of_month(dt):
    first_day = dt.replace(day=1)

    dom = dt.day
    adjusted_dom = dom + first_day.weekday()

    return int(ceil(adjusted_dom/7.0))

db = sqlite3.connect("data/images.sqlite")
db.row_factory=sqlite3.Row
c = db.cursor()

html="<html><body>"
month=''
year=''
timestamp=parse("1933-02-02").date()
#f=open("gallery.json", "w")
images=[]
imageDir="images_original"
for row in c.execute("select * from images  order by CREATEDATE desc"):
	sourceFile=row[4]
        correctedDate=re.sub(r'(\d{4}):(\d{2}):(\d{2}\s+\d{2}:\d{2}:\d{2}).*',r'\1-\2-\3', row[0])
	print correctedDate
	try:
		parsedDate=parse(correctedDate)
	except:
		continue
	if  (parsedDate.year!=year or parsedDate.month!=month):
		year=parsedDate.year
		month=parsedDate.month
		html+="<h3>%s/%s</h3>"%(year, month)
		imageDir="images_original/%s/%s"%(year, month)
		try:
			os.makedirs(imageDir)
		except:
			continue
	md5sum=hashlib.md5("%s:%s:%s:%s:%s"%(parsedDate.year,parsedDate.month, parsedDate.day,parsedDate.hour,parsedDate.minute)).hexdigest()

	delta= relativedelta( timestamp,parsedDate)
#	print delta.years, delta.months,  delta.days, delta.hours
#	print timestamp
#	print parsedDate
	if(delta.years==0 and delta.months==0 and delta.days==0 and delta.hours==0 and delta.minutes<5):
            pass
	else:
		timestamp=parsedDate
		html+= "<img src='images/%s.jpg'></img><br/>"%(md5sum)
                dic=dict(row)
                dic["thumb"]="images/%s_t.jpg"%md5sum
                dic["src"]="images_wide/%s.jpg"%md5sum
                dic["group"]="%d-%d"%(parsedDate.year,parsedDate.month)
                dic["date"]=parsedDate.date().isoformat()
                #dic["group"]="%d-%d-%d"%(parsedDate.year,parsedDate.month,week_of_month(parsedDate))
                images.append(dic)
		sourceFile=dic["SourceFile"].encode("utf-8")
		print sourceFile, md5sum
		if (not os.path.isfile("images/%s_t.jpg"%md5sum)):
			os.system("convert  -auto-orient -thumbnail x300 \"%s\"  images/%s_t.jpg" %(sourceFile, md5sum ))
		if (not os.path.isfile("%s/%s.jpg"%(imageDir, md5sum))):
			os.system("convert \"%s\" -channel rgb -auto-level  -resize 1920x1080^ -gravity center   -auto-orient -quality 86   %s/%s.jpg" %(sourceFile,imageDir,  md5sum ))
		#os.system("convert \"%s\" -channel rgb -auto-level  -resize 1664x936^ -gravity center    -strip -auto-orient -quality 86   images_original/%s.jpg" %(sourceFile, md5sum ))
		
#		if (not os.path.isfile("images_wide/%s.jpg"%md5sum)):
#			cmd="node \"/usr/local/lib/node_modules/smartcrop-cli/smartcrop-cli.js\" --width 1664 --height 936 --minScale 1.0 --maxScale 1.0  images_original/%s.jpg images_wide/%s.jpg "%(md5sum, md5sum) 
	#		os.system(cmd);
#			print "converted"

html+="</body></html>"
f.write("gallery_images="+json.dumps(images))

db.close()


