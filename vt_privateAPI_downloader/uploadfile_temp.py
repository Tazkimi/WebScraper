#! /usr/bin/python
# -*- coding:utf-8 -*-

"""
# @author: lightk
# @date:2018/5/8
# @filename:uploadfile.py
# 功能:上传文件到样本服务器
# 注意****************************注意**************************注意

需要更新本脚本的Cookie(有兴趣可以改进脚本哦)

####################################################################
"""

import re,sys,os
import requests
import json

from requests.packages import urllib3
urllib3.disable_warnings()


def get_files(path):
    for f in os.listdir(path):
        rupath = os.path.join(path, f)
        if os.path.isfile(rupath) and "." not in f:
            yield rupath
        elif os.path.isdir(rupath):
            for p in get_files(rupath):
                yield p

def images(headers,p,url):
    
    files = {'fileToUpload': open(p, 'rb')}
    r = requests.post(url, files=files, headers=headers, verify=False)

    if "html" in r.text:
	    print u"需要修改本脚本的Cookie(在49行),才可以继续下载(有兴趣可以改进脚本,Come On My Baby,Gogogogo!!!!!!!!)"
	    sys.exit(1)
    if "already_check" in r.text:
        print p,u" 已经存在于服务器上"
    else:
        print p,u" 上传成功"
	
def main(pa):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36',
        "Cookie": "mapthink_language=zh-cn; PHPSESSID=8qebbab3n2kvaa5fnseg3qm6i4"
    }

    
    url = 'https://192.168.3.7/index.php?s=/documentsubmit/upload/act/upload/menuid/286/checkFlag//pwd/'

    # p = r"D:\PyWork\Samples\yara\90d17ebd75ce7ff4f15b2df951572653efe2ea17"
    
    for p in get_files(pa):
        images(headers,p,url)
        
    
if __name__ == "__main__":
    pa = r"C:\pywork\Samples"
    main(pa)
    
    
    
    
    
    
