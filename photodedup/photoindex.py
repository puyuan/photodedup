import os.path
import time
import sys
import pickle
# Use the built-in version of scandir/walk if possible, otherwise
# use the scandir module version
try:
        from scandir import walk
except ImportError:
        from os import walk

from os.path import join, isdir, islink


class PhotoIndex():
    def __init__(self):
        self.dict= self._loaddict()

    def regularwalk(self, top):
        epoch=time.time()
        dict=self.dict

        dict['last_accessed_time']=epoch
        root_entries=dict.setdefault('roots', {})
        countfiles=0
        countdirs=0

        for root, dirs, files in walk(top):
            root_entry=root_entries.setdefault(root,[{}, {}, epoch, epoch])
            root_entry[3]=epoch
            
            for dir in dirs:
                path=join(root, dir)
                dir_entry=root_entry[0].setdefault(dir, [path, epoch, epoch])
                dir_entry[2]=epoch
            for file in files:
                if ".jpg" in file.lower():
                    path=join(root, file)
                    file_entry=root_entry[1].setdefault(file, [path, epoch, epoch])
                    file_entry[2]=epoch

            countfiles+=len(files)
            countdirs+=len(dirs)
            sys.stdout.write("Processing %d dirs, %d files \r" %(countdirs, countfiles))
            sys.stdout.flush()
        return dict

    def fetch_new_images(self, root):
        return self.find_images(root)

    def fetch_deleted_images(self, root):
        return self.find_images(root, "deleted")

    def find_images(self, root, image_status="new"):
        new_images_list=[]

        dict=self.dict
        last_accessed_time=dict.get('last_accessed_time', '')
        root_entries=dict.get('roots', {})

        #print dict.get(root)
        dirs, files, create_time, modified_time = root_entries.get(root, [{},{}, 0, 0])
        for name, (path, create_time, modified_time)  in dirs.iteritems():
            if modified_time != last_accessed_time:
                print  (path, modified_time)
        for name, (path, create_time, modified_time)  in files.iteritems():
            if modified_time < last_accessed_time and "deleted"== image_status:
                print path, "file does not exist"
                print modified_time, last_accessed_time
                new_images_list.append(path)
            elif create_time == last_accessed_time and "new" == image_status:
                new_images_list.append(path)


        for name, (path, create_time, modified_time) in dirs.iteritems():
             new_images_list+=self.find_images(path, image_status)
        return new_images_list


    def printdict(self, root):

        dict=self.dict
        last_accessed_time=dict.get('last_accessed_time', '')
        root_entries=dict.get('roots', {})

        #print dict.get(root)
        dirs, files, create_time, modified_time = root_entries.get(root, [{},{}, 0, 0])
        for name, (path, create_time, modified_time)  in dirs.iteritems():
            if modified_time != last_accessed_time:
                print  (path, modified_time)
        for name, (path, create_time, modified_time)  in files.iteritems():
            if modified_time < last_accessed_time:
                print path, "file does not exist"
                print modified_time, last_accessed_time
            elif create_time == last_accessed_time:
                print path, "new_files"


        for name, (path, create_time, modified_time) in dirs.iteritems():
            printDict(dict, path)

    def checkPruning(self,dict):
        last_accessed_time=dict.get('last_accessed_time', '')
        root_entries=dict.get('roots')
        print (last_accessed_time)

        for root, (dirs, files, create_time, modified_time) in root_entries.iteritems():
            if not files:
                continue

            for name, (path, create_time, modified_time)  in dirs.iteritems():
                if modified_time != last_accessed_time:
                    print  (path.encode("utf-8"), modified_time)
            for name, (path, create_time, modified_time)  in files.iteritems():
                print create_time
                if modified_time < last_accessed_time:
                    print path
                elif create_time == last_accessed_time:
                    print path



    def savedict(self):
        dict=self.dict
        output = open('photoindex.pkl', 'wb')
        # Pickle dictionary using protocol 0.
        pickle.dump(dict, output)
        output.close()

    def _loaddict(self):
        try:
            file = open('photoindex.pkl', 'rb')
            # Pickle dictionary using protocol 0.
            output=pickle.load(file)
            file.close()
        except:
            return {}
        return output



