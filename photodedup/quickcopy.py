import sqlite3
import os
import json
import hashlib
import subprocess
from datetime import datetime

def retrieveVal(dic, key):
	if(dic.has_key(key)):
		return dic[key]
	else:
		return "" 

def getExif(file):
    proc = subprocess.Popen("exiftool -n  -json '%s'"%file , stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    try:
        data=json.loads(out)[0]
        return data
    except:
        return None


db = sqlite3.connect("../data/images.sqlite")
c = db.cursor()
images=open("../data/tmp_new_files.txt", "r")
for file in images:
#	for k,v in image.iteritems():
#		print k=="CreateDate"
        file=file.strip()
	file=file.replace("'", "''")
	print file
        c.execute("select SourceFile from images where SourceFile='%s'"%file);
        row=c.fetchone()
        if (row!=None ):
            continue

        image=getExif(file)
        if(image==None):
            continue


	createDate=retrieveVal(image, "CreateDate")
        if(createDate=="" or createDate==None):
            createDate=datetime.now().isoformat(" ")
            print createDate
            continue
	gpsLatitude=retrieveVal(image, "GPSLatitude")
	gpsLongitude=retrieveVal(image, "GPSLongitude")
	gpsAltitude=retrieveVal(image, "GPSAltitude")
	sourceFile=retrieveVal(image, "SourceFile")
	#sourceFile=sourceFile.encode('utf-8')
	md5sum=hashlib.md5(sourceFile.encode('utf-8')).hexdigest()
	#os.system("exiftool -b -ThumbnailImage '%s' > images/%s_t.jpg" %(sourceFile, md5sum ))
        print md5sum
	columns=(createDate, gpsLatitude, gpsLongitude, gpsAltitude, sourceFile)
	print "Inserting %s" %(sourceFile)
	try:
		c.execute("insert into images values (?, ?, ? ,?, ?)", columns)
		db.commit()
#		if (not os.path.isfile("../images/%s_t.jpg"%md5sum)):
#		    os.system("convert  -auto-orient -thumbnail x200 '%s'  ../images/%s_t.jpg" %(sourceFile, md5sum ))
#		if (not os.path.isfile("../images_original/%s.jpg"%md5sum)):
#		    os.system("convert   -resize 1920x1080^ -gravity center   -auto-orient -quality 86 '%s' ../images_original/%s.jpg" %(sourceFile, md5sum ))
	except:
		print "failed to insert, perhaps duplicate"

db.close()
	#c.execute()


