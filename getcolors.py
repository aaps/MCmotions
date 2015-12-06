#!/usr/bin/python -B

import urllib2
from bs4 import BeautifulSoup
import re

baseurl = 'http://minecraft-ids.grahamedgecombe.com/'
cssurl = baseurl + 'stylesheets/bundles/all/1440429950.css'
imageurl = baseurl + 'images/sprites/items-21.png'

headers = { 'User-Agent' : 'Mozilla/5.0' }
htmlreq = urllib2.Request(baseurl, None, headers)
html = urllib2.urlopen(htmlreq).read()
cssreq = urllib2.Request(cssurl, None, headers)
css = urllib2.urlopen(cssreq).read()
# imagereq = urllib2.Request(imageurl, None, headers)
# image = urllib2.urlopen(imagereq).read()



soup = BeautifulSoup(html, "lxml")

for arow in soup.find_all("tr", class_="row"):
	print arow.find("td", {"class": "id"}).get_text()
	tofind = arow.div["class"]
	# print tofind[1]

	match = re.search(r"[^a-zA-Z](" + tofind[1] +  ")[^a-zA-Z]", css)
	num = match.start(1)
	print css[num:num+150]
	print
