#!/usr/bin/env python
# Paul Yuan 2016
import logging
import itertools
import os
import sqlite3

import exifread

from photodedup.fileindex import FileIndex

logger = logging.getLogger()


class PhotoDedup():
    """
    Photodedup deduplicates all image files stored within a directory. It uses sqlite to store exif info for images,
    and uses a built-in fileindex to quickly find new/deleted files.
    """
    def __init__(self, image_folder_path):
        # Create photoindex folder
        photoindexfolder = os.path.join(os.path.expanduser("~"), ".photoindex")
        try:
            os.mkdir(photoindexfolder)
        except:
            logger.debug("Can't make folder")

        # Create SQLlite connection
        self.conn=sqlite3.connect(os.path.join(photoindexfolder, "images.sqlite"))
        self.image_folder_path=image_folder_path
        self.fileindex= FileIndex(image_folder_path)

    def scan_images(self):
        """
        Scan images using the fileindex.
        :return:
        """
        self.fileindex.scanfiles()
        self._insert_images(self.fileindex.get_new_images())
        self._delete_images(self.fileindex.get_deleted_images())

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

    def get_duplicate_images(self):
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
        result = [row[5] for row in cur.execute(sql)]
        return result

    def get_unique_images(self):
        cur = self.conn.cursor()
        sql='''
            select * from images
            group by timestamp
            order by SourceFile
            '''
        result = [row[5] for row in cur.execute(sql)]
        return result

    def print(self, result):
        for image in result:
            print(image)

    def _insert_images(self, new_images):
        cur = self.conn.cursor()
        count = 0
        for meta_data_list in split_every(1000, self.__get_images_metadata(new_images)):

            columns = [(str(d.get("EXIF DateTimeOriginal", d.get("Image DateTime", ""))),
                        str(d.get("EXIF DateTimeOriginal", "")),
                        str(d.get("GPS GPSLatitude", "")),
                        str(d.get("GPS GPSLongitude", "")),
                        str(d.get("GPS GPSAltitude", "")),
                        d.get("SourceFile", "")
                        ) for d in meta_data_list]

            count += len(columns)
            logger.info("Processed %d images..." % count)

            for metadata in meta_data_list:
                logger.debug("inserting %s", metadata.get("SourceFile", ""))

            cur.executemany("insert or ignore into images values (?, ?, ? ,?, ?, ?)", columns)
            self.conn.commit()

    def _delete_images(self, new_images):
        cur = self.conn.cursor()
        count = 0
        for imagelist in split_every(1000, new_images):
            if imagelist:
                columns = [(image,) for image in imagelist]
                cur.executemany("delete from images where SourceFile=?", columns)
                self.conn.commit()


    def __get_images_metadata(self, images):
        for filename in images:
            f=open(filename, "rb")
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


    


