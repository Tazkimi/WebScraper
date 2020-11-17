# !/usr/bin/python
#coding=utf-8
#
# Copyright 2012 Google Inc. All Rights Reserved.

"""Download more than 100 files product of a VT Intelligence search.

VirusTotal Intelligence allows you to download up to the top100 files that
match a given search term. The 100 file limit is a server-side limitation
when creating the file packages. In order to overcome this limitation this
small script has been developed, it will paginate over a given Intelligence
search and download the matching files individually.
"""

__author__ = 'emartinez@virustotal.com (Emiliano Martinez)'


import json
import logging
import optparse
import os
import Queue
import re
import socket
import sys
import threading
import time
import urllib
import urllib2
import shutil
import glob
from MysqlCtr.db_tool import DB_tool

#import requests

# API_KEY = '7558e9f326ffc97f46405da878ca4b011437f489787863afe29916bdb2d5f7da'
API_KEY = 'd8393035cd72faa3ae1d61eb38848a3bcbfe9b5f1472cfa3588ac34e0d7776e0'
INTELLIGENCE_SEARCH_URL = ('https://www.virustotal.com/vtapi/v2/file/search')
INTELLIGENCE_DOWNLOAD_URL = ('https://www.virustotal.com/vtapi/v2/file/download?hash=%s&apikey=%s')

NUM_CONCURRENT_DOWNLOADS = 6
# ./LOCAL_STORE/folder_name/.../file
LOCAL_STORE = 'C:\\pywork\\Samples'

socket.setdefaulttimeout(60)

LOGGING_LEVEL = logging.INFO  # Modify if you just want to focus on errors
logging.basicConfig(level=LOGGING_LEVEL,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    stream=sys.stdout)

            
                    
class Error(Exception):
  """Base-class for exceptions in this module."""


class InvalidQueryError(Error):
  """Search query is not valid."""


def create_download_folder(query=None):
  """Creates a folder to store the downloaded files.

  The Intelligence query issues is stored in a separate txt file inside the
  directory created, this will allow the user to remember the query he performed
  at a later time.

  Args:
    query: the Intelligence search query, as a string, that is issued in order
      to save the corresponding files to the directory being created.

  Returns:
    String with the path of the created folder.
  """
  ## folder_name = time.strftime('%Y%m%dT%H%M%S')
  if not os.path.exists(LOCAL_STORE):
    os.mkdir(LOCAL_STORE)
  folder_path = os.path.join(LOCAL_STORE, folder_name)
  if not os.path.exists(folder_path):
    ## os.mkdir(folder_path)
    os.makedirs(folder_path)
  '''if query:
    query_path = os.path.join(folder_path, 'intelligence-query.txt')
    with open(query_path, 'wb') as query_file:
      query_file.write(query)'''
  return folder_path
TARGET_STORE = 'Z:\\VT'
def move_folder():
  """Creates a folder to store the downloaded files.
  """
  src_path = os.path.join(LOCAL_STORE, folder_name)
  
  if not os.path.exists(TARGET_STORE):
    os.mkdir(TARGET_STORE)

  dst_path = os.path.join(TARGET_STORE, folder_name)
  if not os.path.exists(dst_path):
    os.makedirs(dst_path)
  
  for r,pa,p in os.walk(src_path):
    for n in p:
      # print r,pa
      shutil.copy(os.path.join(r,n),dst_path)
  shutil.rmtree(src_path)
  
def get_matching_files(search, offset=None):
  """Get a page of files matching a given Intelligence search.

  Args:
    search: a VirusTotal Intelligence search phrase. More about Intelligence
      searches at: https://www.virustotal.com/intelligence/help/
    page: a token indicating the page of file results that should be retrieved.

  Returns:
    Tuple with a token to retrieve the next page of results and a list of sha256
    hashes of files matching the given search conditions.

  Raises:
    InvalidQueryError: if the Intelligence query performed was not valid.
  """
  response = None
  offset = offset or ''
  attempts = 0
  parameters = {'query': search, 'apikey': API_KEY, 'offset': offset}
  data = urllib.urlencode(parameters)
  request = urllib2.Request(INTELLIGENCE_SEARCH_URL, data)
  while attempts < 10:
    try:
      response = urllib2.urlopen(request).read()
      ## response = requests.get(INTELLIGENCE_SEARCH_URL, params=parameters)
      break
    except Exception:
      attempts += 1
      time.sleep(1)
  if not response:
    return (None, None)

  try:
    ## response_dict = response.json()
    response_dict = json.loads(response)
  except ValueError:
    return (None, None)

  if not response_dict.get('response_code'):
    raise InvalidQueryError(response_dict.get('error'))

  next_offset = response_dict.get('offset')
  hashes = response_dict.get('hashes', [])
  return (next_offset, hashes)

def download_file(file_hash, destination_file=None):
  """Downloads the file with the given hash from Intelligence.

  Args:
    file_hash: either the md5, sha1 or sha256 hash of a file in VirusTotal.
    destination_file: full path where the given file should be stored.

  Returns:
    True if the download was successful, False if not.
  """
  destination_file = destination_file or file_hash
  download_url = INTELLIGENCE_DOWNLOAD_URL % (file_hash, API_KEY)
  attempts = 0
  
  # proxyIP={'http':'127.0.0.1:1080'}
  # proxy_support = urllib2.ProxyHandler(proxyIP)
  # opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
  # urllib2.install_opener(opener)
  ## return if file exists
  if os.path.exists(destination_file) or \
    len(glob.glob(os.path.join(LOCAL_STORE, folder_name) + '/*/' + file_hash)) > 0:
    return True
  # download_url = 'https://www.virustotal.com/vtapi/v2/file/download'
  # data = {'hash':file_hash,'apikey':API_KEY}
  
  while attempts < 2:
    try:
      # urllib.urlretrieve(download_url, destination_file)
      
      # print download_url
      c = urllib2.urlopen(download_url)
      
      f=open(destination_file,'wb')
      f.write(c.read())
      f.close()
      
      return True
    except Exception,e:
      print str(e)
      attempts += 1
  return False

  
def download_file2(file_hash, destination_file=None):
  """Downloads the file with the given hash from Intelligence.

  Args:
    file_hash: either the md5, sha1 or sha256 hash of a file in VirusTotal.
    destination_file: full path where the given file should be stored.

  Returns:
    True if the download was successful, False if not.
  """
  destination_file = destination_file or file_hash
  download_url = INTELLIGENCE_DOWNLOAD_URL % (file_hash, API_KEY)
  attempts = 0
  
    
  ## return if file exists
  if os.path.exists(destination_file) or \
    len(glob.glob(os.path.join(LOCAL_STORE, folder_name) + '/*/' + file_hash)) > 0:
    return True
  

  
  while attempts < 3:
    try:
      urllib.urlretrieve(download_url, destination_file)
      return True
    except Exception:
      attempts += 1
  return False


def main():
  """Download the top-n results of a given Intelligence search."""
  usage = '''usage: %prog [options] <intelligence_query/local_file_with_hashes>
   
Example: 
python %prog -n 10 -f VT type:"peexe" size:10MB- positives:35+ sources:2+ fs:2016-07-31T01:00:00+ behaviour:"explorer.exe"
python %prog -n 10 -f VT type:"peexe" size:5MB- positives:35+ sources:2+ fs:2016-07-31T01:00:00+ not (kaspersky:infected)
python %prog -n 10 -f VT (type:doc or type:docx or type:xls or type:xlsx or type:docm) (tag:exploit or tag:cve) positives:20+ size:20KB+
python %prog -n 20 -f VT positives:20+ tag:cve-2015-3113
python %prog -n 10 -f pdf type:"pdf" positives:35+ fs:2016-01-01T01:00:00+
python %prog -n 20 -f apk type:"apk" positives:25+ fs:2016-08-01T01:00:00+
python %prog -n 10 -f macros tag:"macros" positives:35+ fs:2016-08-01T01:00:00+
python %prog -n 10 -f VT ./hashes.txt
python %prog -m -n 10 -f VT ./hashes.txt

Modifiers: https://www.virustotal.com/intelligence/help/file-search/#search-modifiers
'''
      
  parser = optparse.OptionParser(usage=usage,
      description='')
  parser.add_option('-n', '--numfiles', dest='numfiles', default=10,
      help='number of files to download')
  parser.add_option('-f', '--foldername', dest='foldername', default='VT',
      help='folder name, e.g. peexe, pdf, doc, xls,,,,,')      
  parser.add_option('-m', action='store_true', dest='is_move',
      help='flag that is or not copy to remote sample machine')  
  (options, args) = parser.parse_args()
  if not args:
    parser.error('No search query provided')

  end_process = False
  search = ' '.join(args)
  search = search.strip().strip('\'')
  numfiles = int(options.numfiles)
  global folder_name 
  folder_name = ''.join(options.foldername)
  print search
  nosearch = False
  if os.path.exists(search):
    with open(search, 'rb') as file_with_hashes:
      content = file_with_hashes.read()
      requested_hashes = re.findall('([0-9a-fA-F]{64}|[0-9a-fA-F]{40}|[0-9a-fA-F]{32})', content)
      search = ','.join(set(requested_hashes))
      ## don't search if args has hash file
      nosearch = True
  #Kaspersky:Trojan-Downloader.VBS.Agent
  db = r'./MysqlCtr/samplehash.db'
  db_tool = DB_tool(db)
  db_tool.connect_db()
  
  logging.info('Starting VirusTotal Intelligence downloader')
  if not nosearch:
    logging.info('* VirusTotal Intelligence search: %s', search)
  logging.info('* Number of files to download: %s', numfiles)

  work = Queue.Queue()  # Queues files to download
  end_process = False

  def worker():
    while not end_process:
      try:
        sha256, folder = work.get(True, 3)
      except Queue.Empty:
        continue
      destination_file = os.path.join(folder, sha256)
      logging.info('Downloading file %s', sha256)
      success = download_file(sha256, destination_file=destination_file)
      if success:
        logging.info('%s download was successful', sha256)
      else:
        logging.info('%s download failed', sha256)
      work.task_done()

  threads = []
  for unused_index in range(NUM_CONCURRENT_DOWNLOADS):
    thread = threading.Thread(target=worker)
    thread.daemon = True
    thread.start()
    threads.append(thread)

  logging.info('Creating folder to store the requested files')
  folder = create_download_folder(search)

  queued = 0
  wait = False
  next_offset = None
  while not end_process:
    try:
      logging.info('Retrieving page of file hashes to download')
      ## don't search if args has hash file
      if not nosearch:
          try:
            next_offset, hashes = get_matching_files(search, offset=next_offset)
          except InvalidQueryError, e:
            logging.info('The search query provided is invalid... %s', e)
            return
      else:
        next_offset, hashes = ('', search.split(','))
        
      if hashes:
        logging.info('Retrieved %s matching files in current page, queueing them',
            len(hashes))
        for file_hash in hashes:
          if db_tool.check_record(file_hash):
            logging.info('The file %s in Database', file_hash)
            continue
          db_tool.save_record_sha256(file_hash)
          
          work.put([file_hash, folder])
          queued += 1
          if queued >= numfiles:
            logging.info('Queued requested number of files')
            wait = True
            break
      if not next_offset or not hashes:
        logging.info('No more matching files')
        wait = True
      if wait:
        logging.info('Waiting for queued downloads to finish')
        while work.qsize() > 0:
          time.sleep(5)
        end_process = True
        for thread in threads:
          if thread.is_alive():
            thread.join()
        logging.info('The downloaded files have been saved in %s', folder)
    except KeyboardInterrupt:
      end_process = True
      logging.info('Stopping the downloader, initiated downloads must finish')
      for thread in threads:
        if thread.is_alive():
          thread.join()
    finally:
      if options.is_move:
        print "..............move files......"
        move_folder()

if __name__ == '__main__':
  main()
  ## sample archive
  #os.system('python ./sample_archiver.py')
  
