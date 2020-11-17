#! /usr/bin/python
#-*- coding:utf-8 -*-

import os,sys
import subprocess


work_dir = "/home/samples_manager/"
def vt_download():
    vt_download_script = os.path.join(work_dir,"vt_privateAPI_downloader.py")
    
    pe_args = 'type:"peexe" size:5MB- positives:30+ sources:2+ fs:2016-01-31T01:00:00+ not (kaspersky:infected)'
    office_args = '(type:doc or type:docx or type:xls or type:xlsx or type:dotm) (tag:exploit or tag:cve) positives:15+ size:10KB+'
    
    
    download_cmd1 = [vt_download_script,"-n 600", "-fVT", pe_args]
    download_cmd2= [vt_download_script,"-n 300","-fVT", office_args] 
    # print download_cmd1,download_cmd2 
    try:
        subprocess.check_call(download_cmd1)
        subprocess.check_call(download_cmd2)
    except subprocess.CalledProcessError:
        print "Error in downloader"
        sys.exit(1)
    
def work():

    static_file_scan = [os.path.join(work_dir,"static_file_scan")]
    kasp_scan =[os.path.join(work_dir,"start_mavscan.sh")]
    samples_preprocess = [os.path.join(work_dir,"samples_preprocess"), os.path.join(work_dir,"input"), os.path.join(work_dir,"output/")]
    kill_task = ["killall","static_file_scan", "start_mavscan.sh", "samples_preprocess", "mav_scan"]
    
    try:
        print "Starting killpre_process"
        subprocess.check_call(kill_task)
    except subprocess.CalledProcessError:
        print "Error in killpre_process"
        sys.exit(1)
    
    try:
        print "Starting samples_preprocess"
        subprocess.Popen(samples_preprocess)
    except subprocess.CalledProcessError:
        print "Error in samples_preprocess"
        sys.exit(1)
    except:
        pass
    
    try:
        print "Starting static_file_scan"
        subprocess.Popen(static_file_scan)
    except subprocess.CalledProcessError:
        print "Error in static_file_scan"
        sys.exit(1)
    
    try:
        print "Starting kasp_scan"
        subprocess.Popen(kasp_scan)
    except subprocess.CalledProcessError:
        print "Error in kasp_scan"
        sys.exit(1)
    
        
def main():
    work_dir = "/home/samples_manager/"
    os.chdir(work_dir)
    vt_download()
    work()
        
if __name__ == '__main__':
    main()
