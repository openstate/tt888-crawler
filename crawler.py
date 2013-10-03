#!/usr/bin/env python

import sys
import os
import re

import codecs
from pprint import pprint

import requests
from BeautifulSoup import BeautifulSoup

def fetch_subtitles(prid):
    try:
        contents = requests.get('http://e.omroep.nl/tt888/%s' % (prid,)).text
    except Exception, e:
        contents = u'No subtitle found'
    
    if contents == u'No subtitle found':
        return False
    
    with codecs.open('subtitles/%s.txt' % (prid,), 'w', 'UTF-8') as outfile:
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
            
    return 0

if __name__ == '__main__':
    sys.exit(main())
