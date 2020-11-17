#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os,sys
from db_tool import DB_tool
from myhash import get_hash
   
def main(db, fpath):
    db_tool = DB_tool(db)
    db_tool.create_db()
    
    for root,path,names in os.walk(fpath):
        for name in names:
            hash = get_hash(os.path.join(root,name))
            db_tool.save_record(*hash)
    
    db_tool.close_connect()
    
if __name__ == '__main__':
    db = 'samplehash.db'
    fpath = "Z:\\office"
    main(db,fpath)