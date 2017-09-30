# Use the built-in version of scandir/walk if possible, otherwise
# use the scandir module version
try:
    from scandir import walk
except ImportError:
    from os import walk

import hashlib
import json
import logging
import os
from os.path import join, expanduser

logger = logging.getLogger()


class FileIndex:
    """
    A file index stores all files contained in a directory, so finding future new and deleted files can become faster.
    Every scan still requires a full scan of the directory, but since only the deltas will be send to downstream processing,
    it can speed up downstream processing time.

    We use the faster os.walk(python >3.5) or scandir.walk, to reduce unnecessary os.stat call.

    The file index includes the list of scanned files and latest new and deleted files.

    """
    def __init__(self, root):
        self.name = hashlib.md5(root.encode("utf8")).hexdigest()
        self.history = set()
        self.tmp_current_scan = set()
        self.newfiles = set()
        self.deletedfiles = set()
        self.root = root

        photoindexfolder = join(expanduser("~"), ".photoindex")
        try:
            os.mkdir(photoindexfolder)
        except:
            logger.debug("Can't make folder")
        self.photoindexpath = join(photoindexfolder, self.name)
        self._loadindex()

    def scanfiles(self):
        """
        Recursively find files in the directory and add to index, specifically to tmp_current_scan.
        When done, a commit is issued which computes the deltas and updates the history
        :param path:
        :return:
        """
        for root, dirs, files in walk(self.root):
            for file in files:
                file_full_path = join(root, file)
                self.tmp_current_scan.add(file_full_path)
        # We are done, commit
        self._commitindex()
        return dict

    def get_new_images(self):
        return list(self.newfiles)

    def get_deleted_images(self):
        return list(self.deletedfiles)

    def _commitindex(self):
        """
        Commit computes the deltas(new files, deleted files), and updates the history list.
        The tmp_current_scan gets reset
        :return:
        """
        self.newfiles = self.tmp_current_scan - self.history
        self.deletedfiles = self.history - self.tmp_current_scan
        self.history |= self.newfiles
        self.history -= self.deletedfiles
        self.tmp_current_scan = set()
        self._saveindex()

    def _getdict(self):
        """
        A helper function for serializing fileindex object
        :return:
        """
        return {
            "history": list(self.history),
            "newfiles": list(self.newfiles),
            "deletedfiles": list(self.deletedfiles)
        }

    def _saveindex(self):
        output = open(self.photoindexpath, 'w')
        json.dump(self._getdict(), output)
        output.close()

    def _loadindex(self):
        try:
            file = open(self.photoindexpath, "r")
            object = json.load(file)
            self.history = set(object["history"])
            self.newfiles = set(object["newfiles"])
            self.deletedfiles = set(object["deletedfiles"])
            file.close()
        except:
            logger.debug("file does not exist")