#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import string
import re
from bs4 import BeautifulSoup
from urlparse import urlparse
import requests
import unicodedata
import time
import sys
import random

host = u"d.pr"
dir = u'./downloads/'

useragent = [i.split('\n') for i in open("ua").readlines()]

def rnd():
    lst = [random.choice(string.ascii_letters + string.digits) for n in xrange(4)]
    ret = "".join(lst)
    return ret
def writelog(txt):
    l=open(u'log.txt','a+b')
    l.write(txt + "\n")
    l.close()

def chk():
    path = u'http://' + host + u"/f/" + rnd()
    writelog(u'path ' + path)
    headerua = { 'User-Agent': random.choice(useragent) }
    writelog(u'useragent: ' + str(headerua))
    q = requests.head(path, headers = headerua)
    status = q.status_code
    writelog(u'status ' + str(status) + '\n\n' + q.content)
    if status == 200:
        content = requests.get(path).content
        if content.find('<section class="image">') > 0:
            page = BeautifulSoup(''.join(content))
            writelog( path + u' - page' + page)
            imgalt = page.findAll('section', {'class':"image"})[0].img['alt']
            print imgalt
            imgsrc = page.findAll('section', {'class':"image"})[0].img['src']
            h = urlparse(imgsrc)
            o=open(dir + unicodedata.normalize('NFKD', imgalt.replace(":","_").replace("\\","_").replace("/","_")).encode('utf-8','ignore'), 'a+b')
            o.write(requests.get(imgsrc).content)
            o.close()
        elif content.find('<section class="text note">') > 0:
            print path + ' - text note'
            writelog(path + u' - text note')
	else:
            print path + ' - file'
            writelog( path + u' - file')
    elif status == 429:
        sys.exit(1)
    return status


while 1:
    chk()
    time.sleep(5)
