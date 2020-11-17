#! /usr/bin/python
# -*- coding:utf-8 -*-

"""
# @author: lightk & yusheng
# @date:2018/5/4
# @filename:threatminer.py
"""

import re,sys
import requests
from bs4 import BeautifulSoup


pdf_domains_all = []
pdf_hosts_all = []
pdf_samples_all = []

def get_content(cturl):
    
    c = requests.get(cturl,headers = headers)
    # print c.text
    
    b = None
    b = BeautifulSoup(c.text,'lxml')
    
    row = b.find_all('div',class_="row tm_row")
    
    if not row:
        print "请用浏览器手动打开链接，检测是否断网啦。。。。"
        sys.exit(1)
    
    for r in row:
        # print r
        # apt_report_1 > table > tbody > tr:nth-child(2) > td:nth-child(2) > a:nth-child(1)
        # pdf_name = r.select_one('table > tr:nth-of-type(2) > td:nth-of-type(1) > a').text
        # print pdf_name

        pdf_domains_tag = r.select('table > tr:nth-of-type(2) > td:nth-of-type(2) > a')
        pdf_hosts_tag = r.select('table > tr:nth-of-type(2) > td:nth-of-type(3) > a')
        pdf_samples_tag = r.select('table > tr:nth-of-type(2) > td:nth-of-type(4) > a')
        
        pdf_domains,pdf_hosts,pdf_samples = None,None,None
        
        if pdf_domains_tag:
            pdf_domains = [d.text for d in pdf_domains_tag]
            pdf_domains_all.extend(pdf_domains)
        if pdf_hosts_tag:
            pdf_hosts = [d.text for d in pdf_hosts_tag]
            pdf_hosts_all.extend(pdf_hosts)
        if pdf_samples_tag:
            pdf_samples = [d.text for d in pdf_samples_tag]
            pdf_samples_all.extend(pdf_samples)
            

        
        # all_tags = []
        # for tag in r.select('table > tr:nth-of-type(2) > td'):
            # all_tags.append(tag.find_all("a"))

def main():
    sturl = 'https://www.threatminer.org/getReport.php?e=report_list_container&t=0&q=%d'
    for q in range(2008,2019):
        print q
        get_content(sturl % q)
    
    dd = {"domains":pdf_domains_all,"hosts":pdf_hosts_all,"samples":pdf_samples_all}
    for k,v in dd.iteritems():
        with open("%s.txt" % k,'w') as pd:
            for x in v:
                pd.write(x+"\n")

if __name__ == '__main__':
    headers = {
     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.114 Safari/537.36'}
    baseurl = 'https://www.threatminer.org/'
    main()
    
    
    
