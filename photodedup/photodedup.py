#!/usr/bin/env python
# Paul Yuan 2016
import os
import sys
import argparse
import sqlite3
import logging
import exifread
import itertools
from  photoindex import PhotoIndex
from logging.config import fileConfig
from os.path import join
import shutil


fileConfig('logging_config.ini')
logger = logging.getLogger()

class PhotoDedup():
    def __init__(self, image_folder_path):
        self.conn=sqlite3.connect("images.sqlite")
        self.image_folder_path=image_folder_path

    def create_index(self):
        logger.info("Create index if not exists")
        cur = self.conn.cursor()
        cur.execute('''create table if not exists images
				 (timestamp text ,
				  CreateDate text,
				  GPSLatitude real,
				  GPSLongitude   real,
				  GPSAltitude    real ,
				  SourceFile   text,
				  PRIMARY KEY (timestamp, SourceFile)
				  )''')



    def insert_images(self, new_images):
        cur = self.conn.cursor()
        count=0
        for metadataList in split_every(1000, self.__get_images_metadata(new_images)):

            columns = [(str(d.get("EXIF DateTimeOriginal", d.get("Image DateTime", ""))),
                        str(d.get("EXIF DateTimeOriginal", "")),
                        str(d.get("GPS GPSLatitude", "")),
                        str(d.get("GPS GPSLongitude", "")),
                        str(d.get("GPS GPSAltitude", "")),
                        d.get("SourceFile", "")
                        ) for d in metadataList]

            count+=len(columns)
            logger.info("Processed %d images..." % count )

            for metadata in metadataList:
                logger.debug("inserting %s", metadata.get("SourceFile", ""))


            cur.executemany("insert or ignore into images values (?, ?, ? ,?, ?, ?)", columns)
            self.conn.commit()

    def remove_images(self, new_images):
        cur = self.conn.cursor()
        count=0
        for imagelist in split_every(1000, new_images):
            print imagelist
            if imagelist:
                columns = [(image,) for image in imagelist]
                cur.executemany("delete from images where SourceFile=?", columns)
                self.conn.commit()

    def find_duplicate(self):
        cur = self.conn.cursor()
        sql='''
            select * from images
            where timestamp in (
            select timestamp from images
            where timestamp != ""
            group by timestamp
            having count(*)>1)
            except
            select *
            from images
            group by timestamp
            '''
        for row in cur.execute(sql):
            print row[5].encode('utf-8')



    def __get_images_metadata(self, images):
        for filename in images:
            f=open(filename)
            tags = exifread.process_file(f, details=False)
            tags["SourceFile"]=filename
            yield tags
            f.close()

def split_every(n, iterable):
    i = iter(iterable)
    piece = list(itertools.islice(i, n))
    while piece:
        yield piece
        piece = list(itertools.islice(i, n))

# TODO
def get_parser():
    parser = argparse.ArgumentParser(description='photo deduplication tool')

    parser.add_argument('-d', '--duplicate', help='list duplicate images', action='store_true')
    parser.add_argument('-u', '--unique', help='list unique images',
                        action='store_true')
    parser.add_argument('image_path')

    return parser
               


parser=get_parser()
args=vars(parser.parse_args())
if args["duplicate"]:
    image_path=unicode(args['image_path'])
    photoDedup=PhotoDedup(image_path)
    photoDedup.create_index()
    photoIndex=PhotoIndex()
    photoIndex.regularwalk(image_path)
    photoIndex.savedict()
    deleted_images=photoIndex.fetch_deleted_images(image_path)
    photoDedup.remove_images(deleted_images)
    new_images=photoIndex.fetch_new_images(image_path)
    photoDedup.insert_images(new_images)
    photoDedup.find_duplicate()


