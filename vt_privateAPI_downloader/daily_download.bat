@echo off

::by lightk

echo ��ǰĿ¼: %CD%
set ocd=%CD%


cd /d C:\pywork
echo ��ǰĿ¼: %CD%

rem ��ȡ��ǰ����
set n_date=%date:~0,10%
set nn_date=%n_date:/=%


python vt_privateAPI.py -n 200 -m -f bit64%nn_date% tag:64bits eset_nod32:infected positives:15+ fs:2015-05-01T01:00:00+ >> log.txt
python vt_privateAPI.py -n 300 -m -f exe%nn_date% type:"peexe"  positives:15+ eset_nod32:infected  fs:2015-05-01T01:00:00+ >> log.txt
python vt_privateAPI.py -n 100 -m -f cveoffice%nn_date% type:doc or type:docx or type:xls or type:xlsx or type:ppt or type:pptx or type:rtf tag:exploit or tag:cve positives:15+ size:20KB+ fs:2015-05-01T01:00:00+ >> log.txt
::python vt_privateAPI.py -n 1100 -f maloffice%nn_date% type:doc or type:docx or type:xls or type:xlsx or type:ppt or type:pptx or type:rtf positives:15+ size:20KB+ fs:2017-01-01T01:00:00+ >> log.txt

cd /d %ocd%
echo ��ǰĿ¼: %CD%

::pause>NUL

@echo on