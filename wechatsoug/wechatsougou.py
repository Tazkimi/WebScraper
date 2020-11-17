#! /usr/bin/python
# -*- coding:utf-8 -*-

"""
# @author: lightk
# @date:2018/2/08
# @filename:wechatsougou.py
"""

import re,sys,time
import requests
from bs4 import BeautifulSoup
from json import loads


def get_url(sturl):
    curls = []
    try:
        c = requests.get(sturl,headers = headers)
    except Exception as e:
        print sturl,str(e)
        return curls
    b = None
    b = BeautifulSoup(c.text,'lxml')
    
    w_url_tag = b.select_one('#sogou_vr_11002301_box_0 > div > div.txt-box > p.tit > a')
    
    curl = w_url_tag.attrs["href"]
    # print curl
    return curl
    

def get_content(cturl,w_id):
    
    c = requests.get(cturl,headers = headers)
    # print c.text
    
    b = None
    b = BeautifulSoup(c.text,'lxml')
    # print to_pp_string(b.text)
    
    a = re.search(r'var msgList = (\{"list"\:\[\{".*\]\});',b.text)
    
    if a is None:
        print "请用浏览器手动打开链接，并输入验证码继续。。。。"
        sys.exit(1)
    
    da = loads(a.group(1))
    
    print "*" * 30 , wechat_accounts[w_id].decode("utf-8"), "*" * 30
    
    with open('%s.md' % wechat_accounts[w_id].decode("utf-8").encode("gbk"),'w') as ff:
        ff.write("#%s#" % wechat_accounts[w_id])
        ff.write("\n")
        ff.write("\n")
        for c in  da["list"]:
            cc =  c['app_msg_ext_info']
            ff.write("- 标题:"+cc['title'].replace('&amp;','&').encode("utf-8",'ignore'))
            ff.write("\n")
            ff.write('- 摘要:'+cc['digest'].encode("utf-8",'ignore'))
            ff.write("\n")
            ff.write("- [URL]("+baseurl+cc['content_url'].replace('&amp;','&').encode("utf-8",'ignore')+")")
            ff.write("\n")
            ff.write("\n")
            ff.write('-' * 80)
            ff.write("\n")
            ff.write("\n")
            ff.write("\n")
            # print "id:",cc['fileid']
            # print "title:",cc['title'].replace('&amp;','&').encode("gbk")
            # print 'digest:',cc['digest'].replace('&amp;','&').encode("gbk","ignore")
            # print "url:",baseurl+cc['content_url'].replace('&amp;','&').encode("gbk")
            # print '-' * 80

def main(wechat_accounts):
    sturl = 'http://weixin.sogou.com/weixin?type=1&s_from=input&query=%s&ie=utf8&_sug_=n&_sug_type_='
    for w_id in wechat_accounts.keys():
        cturl = get_url(sturl % w_id)
        get_content(cturl,w_id)
        time.sleep(3)

if __name__ == '__main__':
    headers = {
     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.114 Safari/537.36'}
    baseurl = 'https://mp.weixin.qq.com'
    wechat_accounts = {'gh_a7c4e5da475e': "兰云科技", "python6359":"python"} # ,'gh_a7c4e5da475e'
    main(wechat_accounts)
