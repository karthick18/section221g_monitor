#!/usr/bin/env python

import os, sys, time
from sendmail import send_mail
last_case_name = 'section_221g_last_case_status.pdf'
cur_case_name = 'section_221g_cur_case_status.pdf'
url_prefix = 'http://photos.state.gov/libraries/'#201202/june2012/adprocases20120625.pdf
casestatus_prefix = 'adprocases'
url_list = []
ltime = time.localtime(time.time())
yprefix = '02'
year_prefix = time.strftime('%Y', ltime).strip() + yprefix
url_list.append(year_prefix)
month_year = time.strftime('%B%Y', ltime).strip().lower()
url_list.append(month_year)
case_url = casestatus_prefix + time.strftime('%Y%m%d', ltime) + '.pdf'
url_list.append(case_url)

section_221g_url = url_prefix + '/'.join(url_list)
print 'url = [%s]' %section_221g_url

os.rename(cur_case_name, last_case_name)
os.system('wget %s -O %s' %(section_221g_url, cur_case_name))

if os.stat(cur_case_name).st_size == 0:
    os.rename(last_case_name, cur_case_name)
    print 'Unable to fetch case data from [%s]' %section_221g_url
    sys.exit(0)

last_case_txt_file = last_case_name.split('.')[0] + '.txt'
cur_case_txt_file =  cur_case_name.split('.')[0] + '.txt'

os.system('pdftotext -layout %s %s' %(last_case_name, last_case_txt_file))
os.system('pdftotext -layout %s %s' %(cur_case_name, cur_case_txt_file))
print 'Processing section 221g case list pertaining to last case file [%s] and current file [%s]' %(
    last_case_txt_file, cur_case_txt_file)
os.system('./parse_221g.py %s %s > %s' %(last_case_txt_file, cur_case_txt_file, 'case_status'))

send_mail('c3po-z1@openclovis.com', 'karthick@openclovis.com', 'Visa case status', 
          file('case_status').read())
