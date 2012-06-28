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

tracked_cases = {'2012156-291-1':('PENDING_PROCESS', 'PENDING_PROCESS')}
def parse_221g(last_txt_file, new_txt_file):
    last_lines = open(last_txt_file, 'r').readlines()
    last_cases = {}
    changed_cases = {}
    case_status_map = {}
    case_status_body = ''
    parse_line = False
    for l in last_lines:
        l1 = l.strip()
        if not parse_line:
            if l1.find('BATCH ID') >= 0:
                parse_line = True
            continue

        ## get case id
        case_id = '-'.join(l1.split()[:3]).strip()
        case_status = '_'.join(l1.split()[3:]).strip()
        last_cases[case_id] = case_status
        
    parse_line = False
    new_lines = open(new_txt_file, 'r').readlines()
    for l in new_lines:
        l1 = l.strip()
        if not parse_line:
            if l1.find('BATCH ID') >= 0:
                parse_line = True
            continue

        case_id =  '-'.join(l1.split()[:3]).strip()
        case_status = '_'.join(l1.split()[3:]).strip()
        if case_id in last_cases.keys():
            if case_status != last_cases[case_id]:
                changed_cases[case_id] = (last_cases[case_id], 
                                          case_status )
                if case_id in tracked_cases.keys():
                    tracked_cases[case_id] = (last_cases[case_id],
                                              case_status ) #update tracked case status

                status = case_status.lower()
                if not case_status_map.has_key(status):
                    case_status_map[status] = []

                case_status_map[status].append(case_id)

    case_status_body += 'Case status changed for [%d] cases\n' %len(changed_cases.keys())
    for status in case_status_map.keys():
        case_status_body += 'Cases %s: [%d]\n' %(status, len(case_status_map[status]))
    case_status_body += '\n'
    items = changed_cases.items()
    items.sort()
    for id, status in items:
        case_status_body += 'Case [%s] status changed from [%s] to [%s]\n' %(id, status[0], status[1])

    case_status_body += '\n\nTracked cases status:\n'
    track_hits = 0
    for t in tracked_cases.keys():
        last_status = tracked_cases[t][0]
        cur_status =  tracked_cases[t][1]
        if last_status != cur_status:
            track_hits = track_hits + 1
            case_status_body += 'Case [%s] being tracked has changed from [%s] to [%s]\n' %(
                t, last_status, cur_status)
        else:
            case_status_body += 'Case [%s] status remains unchanged\n' %t

    case_status_subject = 'Visa case status'
    if track_hits:
        case_status_subject += ' (Tracked cases hits: %d)' %track_hits

    return (case_status_subject, case_status_body)

subject, body = parse_221g(last_case_txt_file, cur_case_txt_file)
# dump the body to a case status file for a sample mail format
file('case_status', 'w').write(body)
send_mail('c3po-z1@openclovis.com', 'karthick@openclovis.com', subject, body) 
