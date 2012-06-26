#!/usr/bin/env python
import os, sys

tracked_case_list = ['2012156-291-1']

def parse_221g(last_txt_file, new_txt_file):
    last_lines = open(last_txt_file, 'r').readlines()
    last_cases = {}
    changed_cases = {}
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

    print 'Case status changed for [%d] cases\n' %len(changed_cases.keys())
    for id, status in changed_cases.items():
        print 'Case [%s] status changed from [%s] to [%s]' %(id, status[0], status[1])

    print '\n\nTracked cases status:\n'
    for t in tracked_case_list:
        if t not in changed_cases.keys():
            print 'Case [%s] status remains unchanged' %t
        else:
            print 'Case [%s] being tracked has changed from [%s] to [%s]' %(
                t, changed_cases[t][0], changed_cases[t][1])
            
if len(sys.argv) < 3:
    sys.exit(127)

last_txt_file = sys.argv[1].strip()
new_txt_file = sys.argv[2].strip()
if __name__ == '__main__':
    #print 'Parsing section 221g information with new case file [%s], last case file [%s]' %\
    #(new_txt_file, last_txt_file)
    parse_221g(last_txt_file, new_txt_file)
