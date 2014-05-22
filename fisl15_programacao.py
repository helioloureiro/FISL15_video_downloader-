#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
System to get titles and authors from FISL15 presentations,
and match them to video files, already downloaded.

To download all videos (18 GB): 
    wget -nH -np -r --mirror http://hemingway.softwarelivre.org/fisl15/high/

Presentations grid:
    http://papers.softwarelivre.org/papers_ng/public/new_grid?day=9
    
LICENSE:
    "THE BEER-WARE LICENSE" (Revision 42):
    Helio Loureiro wrote this file. As long as you retain this notice you
    can do whatever you want with this stuff. If we meet some day, and you think
    this stuff is worth it, you can buy me a beer in return.
    Helio Loureiro"

    helio@loureiro.eng.br
"""
from BeautifulSoup import BeautifulSoup
import urllib2
import re
import os
import sys

URL="http://papers.softwarelivre.org/papers_ng/public/new_grid?day="
DAYS = [7, 8, 9, 10]
# My directory to find videos.  Probably you need to fix it.
TARGETDIR = "%s/Videos/FISL15" % os.environ.get('HOME')

if not os.path.exists(TARGETDIR + "/TODOS"):
    os.mkdir(TARGETDIR + "/TODOS")
    
for day in DAYS:
    page = urllib2.urlopen("%s%d" %(URL, day))
    soup = BeautifulSoup(page.read())

    for html  in soup.findAll('div', "slot-list"):
        for d in html.findAll('div'):
            a = d.find('div', "author")
            t = d.find('div', "title")
            l = d.find('a')
            
            # if empty info, move on
            if not a or not t or not l:
                continue
            
            # wordlist clean up
            author = re.sub("\n", "", a.string)
            author = re.sub("  ","", author)
            title = re.sub("\n", "", t.string)
            title = re.sub("  ", "", title)
            title = re.sub("/", "", title) #avoiding directory issues
            link = l.get('href')
            
            # since wget kept the directory structure, it is easy
            dirvideo = re.sub("http://hemingway.softwarelivre.org", TARGETDIR, link)
            
            # is the video over there?  
            status = False
            if os.path.exists(dirvideo):
                status = True
            # False here could trigger urllib2 to download video

            print author, ",",
            print title, ",", 
            print link, ",",
            print status
    
            if status:
                videoname = "%s/TODOS/%s - %s.ogv" % (TARGETDIR, title, author)
                if os.path.exists(videoname):
                    continue
                try:
                    os.link(dirvideo, videoname)
                except:
                    # Added this because titles w/ strings "/" where causing issues,
                    # so I had to check.  GNU/Linux was the problem (Stallman's fault).
                    print "Failed to link %s to %s" % (dirvideo, videoname)
                    sys.exit(1)
                print "Created: %s" % videoname
                