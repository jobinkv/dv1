#!/usr/bin/python
import scipy.io as sio
import os
import numpy as np
import cgi, cgitb 
import jinja2
import ipdb
import random
'''read the annotation file'''
def readAnnotation(file_name):
    with open(file_name, 'r') as data:
        x = []
        y = []
        for line in data:
            p = line.split('\t')
            x.append(p[0])
            y.append(p[1])
    return x, y

def readDataset(file_name):
    with open(file_name, 'r') as data:
        x = []
        for line in data:
            p = line.split('\t')
            x.append(p[0])
    return x
#ipdb.set_trace()
'''Input of the system'''
[imgs,labels]=readAnnotation('annotation.txt')
dataset = readDataset('2013.txt')
outData=[]
cnt=0
MaxNo = 50
#shown = readDataset('shownImages.txt')
#fullShown = shown+imgs
#file = open("shownImages.txt","a") 
for i in range(0,100000):
	datImg = random.choice(dataset).split('\n')[0]
	if datImg not in imgs:
		outData.append(datImg)
#		file.write(datImg+'\n') 
		cnt=cnt+1	
	if cnt>MaxNo:
		break
#file.close()

#ipdb.set_trace()

#print "</html>"
templ = '''Content-type:text/html\r\n\r\n
<!DOCTYPE html>
<html>
<head>
<style>
table {font-family: arial, sans-serif;border-collapse: collapse;width: 100  %;}
td, th {border: 3px solid #dddddd;text-align: left;padding: 8px;}
tr:nth-child(all) {background-color: #dddddd;}
</style>
</head>
<body>
<table>
<tr>
	<th>
		Sl No
	</th>
	<th>
		Item
	</th>
	<th>
		Choose any image
	</th>
</tr>
        {% for slno, img in lst %}
<tr>
	<td>
		{{slno}}
	</td>
	<td>
		<figure>
			<img src="/pdfFig2/subImg/{{img}}">
			<figcaption>Image name: {{img}}</figcaption>
		</figure>
	</td>
	<td>
		<form action="s2.py" method="get"> 						
		<input type="checkbox" style="zoom:3" name="v" 
		value="{{img}}">Select this image 
		<input type="submit" style="zoom:3" value="Submit">
	</td>
</tr>
            {% endfor %}
</table>
</body>
</html>'''

slnos=list(np.arange(len(outData)))
lst = zip(slnos,outData)
template = jinja2.Template(templ)
print template.render(lst=lst)
