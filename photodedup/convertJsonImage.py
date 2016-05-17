import sqlite3
import os
import json
import hashlib
from dateutil.parser import parse
from dateutil.relativedelta import *
from math import ceil
import re

db = sqlite3.connect("../data/images.sqlite")
db.row_factory=sqlite3.Row
c = db.cursor()

images=[]
for row in c.execute("select * from images order by CREATEDATE desc"):
    print row["SourceFile"].encode("utf8")

