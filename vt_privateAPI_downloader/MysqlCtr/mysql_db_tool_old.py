#! /usr/bin/python
#-*- coding:utf-8 -*-


import MySQLdb as mdb

# �������ݿ�
# conn = mdb.connect('192.168.3.7', 'root', '123456')

# Ҳ����ʹ�ùؼ��ֲ���
# conn = mdb.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='test', charset='utf8')

# Ҳ����ʹ���ֵ�������Ӳ����Ĺ���
config = {
    'host': '192.168.3.7',
    'port': 3306,
    'user': 'root',
    'passwd': 'smp123',
    'db': 'virus_samples',
    'charset': 'utf8'
}


class MysqlTool(object):
    def __init__(self, config):
        self.db = db
        self.conn = None
        self.cursor = None
        self.config = config
        self.connect_cursor()
        
    def connect_cursor(self):
        self.conn = mdb.connect(**self.config)
        self.cursor = conn.cursor()
        
    def save_sample_info(self,data):
        sql = "insert into sample_info(sample_id,sample_md5,sample_sha1,sample_sha256,sample_name,file_size,file_type,file_path) values(%s,%s,%s,%s,%s,%s,%s,%s)"
        param = data
        n = cursor.execute(sql, param)
    

    def save_static_info(self,data):
        sql = "insert into sample_static_info(sample_id,oep,op_segment,sample_create_time,import_hash,subsystem) values(%s,%s,%s,%s,%s,%s)"
        param = data
        n = cursor.execute(sql, param)
    
    def change_static_status(self,id): 
        sql = "update?user?set?static_status=1?where?sample_id=%s"
        param = (id)
        n=cursor.execute(sql,param)

        
    def save_section_info(self, data):
        sql = "insert into sample_section_info(sample_id,section_name,virtual_address,virtual_size,raw_address,raw_size,characteristics,entropy) values(%s,%s,%s,%s,%s,%s,%s,%s)"
        param = data
        n = cursor.execute(sql, param)
        
    def save_imports(self,data):
        sql = "insert into sample_imports(sample_id,) values(%s,%s)"
        param = data
        n = cursor.execute(sql, param)    
    


    
    def close_connect(self):
        if self.cursor:
            self.cursor.close()
        
        if self.conn:
            self.conn.commit()
            self.conn.close()    
        
        
        
        
        
        
        
        
try:
    cursor.execute('select * from av_result limit 25')
    # print 'total records: %d' % cursor.count
    print 'total records:', cursor.rowcount

    # ��ȡ������Ϣ
    desc = cursor.description
    print "%s %3s" % (desc[0][0], desc[1][0])

    # ��ѯһ����¼
    print 'fetch one record:'
    result = cursor.fetchone()
    print result
    print 'id: %s,name: %s' %(result[0],result[1])

    # ��ѯ������¼
    print 'fetch five record:'
    results = cursor.fetchmany(5)
    for r in results:
        print r

except:
    import traceback
    traceback.print_exc()
    # ��������ʱ���
    conn.rollback()
finally:
    # �ر��α�����
    cursor.close()
    # �ر����ݿ�����
    conn.close()



