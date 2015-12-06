#!/usr/bin/python -B

import urllib2
from bs4 import BeautifulSoup
import re
from PIL import Image
import StringIO
import ast



baseurl = 'http://minecraft-ids.grahamedgecombe.com/'
cssurl = baseurl + 'stylesheets/bundles/all/1440429950.css'
imageurl = baseurl + 'images/sprites/items-21.png'

headers = { 'User-Agent' : 'Mozilla/5.0' }
htmlreq = urllib2.Request(baseurl, None, headers)
html = urllib2.urlopen(htmlreq).read()
cssreq = urllib2.Request(cssurl, None, headers)
css = urllib2.urlopen(cssreq).read()
imagereq = urllib2.Request(imageurl, None, headers)
image = urllib2.urlopen(imagereq).read()

buff = StringIO.StringIO(image)


im = Image.open(buff)

print im.size, im.mode

soup = BeautifulSoup(html, "lxml")
counter = 0

for arow in soup.find_all("tr", class_="row"):
	
	tofind = arow.div["class"]
	name = arow.find_all("span", class_="name")[0].getText()
	match = re.search(r"[^a-zA-Z](" + tofind[1] +  ")[^a-zA-Z]", css)
	num = match.start(1)
	if len( css[num:num+110].split(" ")[2][1:-2]) > 2:
		dimtoget = ast.literal_eval(css[num:num+110].split(" ")[2][1:-2])
		cromdim = (0,dimtoget,32,dimtoget+32)
		allcolors = im.crop(cromdim).getcolors()
		tofind = arow.find_all("td", class_="id")[0].getText().split(":")
		if len(tofind) < 2:
		 	tofind.append("0")
		newcolors = []
		if allcolors:
			for color in allcolors:
				if color[1][3] > 0:
					for x in xrange(1,color[0]):
						
						newcolors.append((color[1][0], color[1][1], color[1][2]))

			print ( ":".join(tofind) + " - " + name + " - " + str(tuple(map(lambda y: round(sum(y) / float(len(y))/255, 3), zip(*newcolors)))))


