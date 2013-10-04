#!/usr/bin/env python

import sys
import os
import re

import codecs
from pprint import pprint
from time import sleep

import requests
from BeautifulSoup import BeautifulSoup

def fetch_program_info(prid):
    try:
        contents = requests.get('http://e.omroep.nl/metadata/aflevering/%s' % (prid,)).text
    except Exception, e:
        return False
    
    file_name = 'program_info/%s.json' % (prid,)
    if os.path.exists(file_name):
        return False

    with codecs.open(file_name, 'w', 'UTF-8') as outfile:
        outfile.write(contents)

    return True

def fetch_subtitles(prid):
    try:
        contents = requests.get('http://e.omroep.nl/tt888/%s' % (prid,)).text
    except Exception, e:
        contents = u'No subtitle found'
    
    if contents == u'No subtitle found':
        return False
    
    file_name = 'subtitles/%s.txt' % (prid,)
    if os.path.exists(file_name):
        return False

    with codecs.open(file_name, 'w', 'UTF-8') as outfile:
        outfile.write(contents)

    return True

def main():
    try:
        contents = requests.get('http://www.npo.nl/uitzending-gemist').text
    except Exception, e:
        contents = u''
    
    if contents == u'':
        return 1
    
    soup = BeautifulSoup(contents)
    prids = [l['href'].replace('/programmas/', '') for l in soup.findAll('a', href=re.compile(r'\/programmas\/'))]

    for prid in prids:
        if fetch_subtitles(prid):
            print prid
            sleep(1)
            fetch_program_info(prid)
            sleep(1)
            
    return 0

if __name__ == '__main__':
    sys.exit(main())
