#!/usr/bin/env python
#-*- coding:utf-8 -*-


import os,sys
import hashlib
from collections import namedtuple as ntuple

def get_hash(fp):

    md5 = hashlib.md5()
    sha1 = hashlib.sha1()
    sha256 = hashlib.sha256()
    sha512 = hashlib.sha512()
    
    Hash = ntuple('hash',['md5','sha1','sha256','sha512'])
    
    with open(fp, 'rb') as fb:
        while True:
            blk = fb.read(8192) # 8KB per block
            if not blk: break
            md5.update(blk)
            sha1.update(blk)
            sha256.update(blk)
            sha512.update(blk)
            
    return Hash(md5.hexdigest(),sha1.hexdigest(),sha256.hexdigest(),sha512.hexdigest())
    # return sha512.hexdigest(),

if __name__ == '__main__':
    # fp = r"D:\PyWork\Samples\VT\234E22D3B7BBA6C0891DE0A19B79D7EA"
    
    if len(sys.argv) == 2 and os.path.isfile(sys.argv[1]):
        pass
    else:
        print "\nUsage: \n\tpython %s filename" % sys.argv[0]
        sys.exit(1)
    
    hash = get_hash(sys.argv[1])
    print "\n".join(hash)