#!/usr/bin/env python
#-*- coding:utf-8 -*-


import sys
import sqlite3


class DB_tool:

    def __init__(self, db):
        self.db = db
        self.conn = None
        self.connect_db()
    
    def create_db(self):
        self.conn = sqlite3.connect(self.db)
        
        table_str = '''CREATE TABLE SAMPLE
               (ID INTEGER PRIMARY KEY  AUTOINCREMENT   NOT NULL,
               MD5            TEXT      NOT NULL,
               SHA1           TEXT    NOT NULL,
               SHA256         TEXT     NOT NULL
               );'''
        try:
            self.conn.execute(table_str)
            self.conn.commit()
        except sqlite3.OperationalError:
            pass
        
    def connect_db(self):
        self.conn = sqlite3.connect(self.db)
        
    def check_record(self, uhash):
        len_hash = {
        40:"SHA1",
        32:"MD5",
        64:"SHA256"
        }
        uhash = uhash.strip()
        try:
            hash_type = len_hash[len(uhash)]
        except KeyError,e:
            print "Wrong hash value %s" % uhash
        
        search_str = "SELECT id from SAMPLE WHERE {0}='{1}';".format(hash_type,uhash)
        cursor = self.conn.execute(search_str)
        if cursor.fetchone():
            return True
        return False
        
    def save_record(self,md5,sha1,sha256):
        if not self.check_record(md5):
            insert_str = "INSERT INTO SAMPLE (MD5,SHA1,SHA256) VALUES ('{0}', '{1}', '{2}');".format(md5,sha1,sha256)
            self.conn.execute(insert_str)
            self.conn.commit()
            
    def save_record_sha256(self, sha256):
        sha256 = sha256.strip()
        if not self.check_record(sha256):
            insert_str = "INSERT INTO SAMPLE (MD5,SHA1,SHA256) VALUES ('{0}', '{1}', '{2}');".format("not","not",sha256)
            self.conn.execute(insert_str)
            self.conn.commit()
        

    def search_record(self, uhash):
        len_hash = {
        40:"SHA1",
        32:"MD5",
        64:"SHA256"
        }
        uhash = uhash.strip()
        try:
            hash_type = len_hash[len(uhash)]
        except KeyError,e:
            print "Wrong hash value %s" % uhash
        
        search_str = "SELECT * from SAMPLE WHERE {0}='{1}';".format(hash_type,uhash)
        cursor = self.conn.execute(search_str)
        row = cursor.fetchone()
        if row:
            print row
        else:
            print "not in database"
            
    def close_connect(self):
        if self.conn:
            self.conn.close()
            
def main(db):
    db_tool = DB_tool(db)
    db_tool.create_db()
    
    if len(sys.argv) == 2:
        db_tool.search_record(sys.argv[1])

if __name__ == '__main__':
    db = 'samplehash.db'
    main(db)
    
    
    
    
    
    
    
    
    
    
    
