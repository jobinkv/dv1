#!/usr/bin/python
import scipy.io as sio
import os
import numpy as np
import cgi, cgitb 
import jinja2
import ipdb
import csv 
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

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
'''read the annotation file'''
def readAnnotationWkey(file_name,key):
    with open(file_name, 'r') as data:
        x = []
        for line in data:
            p = line.split('\t')
            if key==p[1].split('\n')[0]:
               x.append(p[0])
    return x

'''read classification data'''
def readClassification(file_name):
    ifile = open(file_name, "rb")
    return csv.reader(ifile)
#ipdb.set_trace()
#[imgs,labels]=readAnnotation('annotation.txt')
'''Input of the system'''

# Create instance of FieldStorage 
form = cgi.FieldStorage() 
# Get data from fields
key = form.getvalue('k')
bigin = int(form.getvalue('sp'))
batchsize = int(form.getvalue('ni'))
ticmark = int(form.getvalue('c'))
'''
key = 20# form.getvalue('k')
bigin = 692# int(form.getvalue('sp'))
batchsize = 1 # int(form.getvalue('ni'))
ticmark = 0 # int(form.getvalue('c'))
'''

if ticmark==1:
	c='checked'
else:
	c=' '
csvred = readClassification('machineannotation-v4.txt')
sortedlist = sorted(csvred, key=lambda row: row[int(key)], reverse=True)
Imagelist=[]
cnt=0
starter=0
[imgs,labels]=readAnnotation('annotation.txt')
for row in sortedlist:
	starter=starter+1
	if starter>=bigin:
		if row[0] not in imgs:
			Imagelist.append(row[0])
			cnt=cnt+1
		if cnt==batchsize:
			break
#	print row[0]
#ipdb.set_trace()
#Imagelist=readAnnotation('annotation.txt',key)
#for itm in Imagelist:
#	print "<h3>The query image name %s</h3>" % (itm)
	#print itm
#checked
#print "</body>"
#print "</html>"
templ = '''Content-type:text/html\r\n\r\n
 <html>
<head>
</head>
<body> 
    <center>
        <table border="2" cellspacing="1">
<form action="s3v1.py" method="post">
	<tr><td>Sl.No</td><td>Automatically choosen Images</td><td>Select a label 
</td>
</tr>
	
        {% for slno, img in lst %}
            <tr>
                <td>
		{{slno}} 
                </td>
                <td>
		<img src="/pdfFig2/subImg/{{img}}">
		<figcaption>Image name: {{img}}</figcaption>
                </td>
		<td>
  <input type="checkbox" style="zoom:3" name="id" value={{img}} {{c}}><br>
		</td>
            </tr>
            {% endfor %}
	<tr><td>End</td>
	<td>
		Select a label 
		<select style="zoom:2" name="label">
<option value="Sketches">Sketches</option>
<option value="Block diagram">Block diagram</option>
<option value="Combined images">Combined images</option>
<option value="Mask">Mask</option>
<option value="Heat map">Heat map</option>
<option value="Pie chart">Pie chart</option>
<option value="Tables">Tables</option>
<option value="Combined plots">Combined plots</option>
<option value="Bar plots">Bar plots</option>
<option value="Algorithm">Algorithm</option>
<option value="Flow chart">Flow chart</option>
<option value="Scatter plot">Scatter plot</option>
<option value="Graph plots">Graph plots</option>
<option value="Confusion matrix">Confusion matrix</option>
<option value="3D objects">3D objects</option>
<option value="Medical images">Medical images</option>
<option value="Natural images">Natural images</option>
<option value="Box plot">Box plot</option>
<option value="Vector plot">Vector plot</option>
<option value="Polar plot">Polar plot</option>
<option value="Histogram">Histogram</option>
</select>
	</td>
	<td>
		<input type="submit" style="zoom:3" value="Submit">
	</td> 
	</tr>
	</form>
        </table>
    </center>
    </body>
</html>'''

slnos=list(np.arange(len(Imagelist)))
#let = ["2010_05539963-Figure1-1subFig-4.png", '2010_05539963-Figure1-1subFig-4.png', '2010_05539963-Figure1-1subFig-4.png', '2010_05539963-Figure1-1subFig-4.png']

lst = zip(slnos,Imagelist)
template = jinja2.Template(templ)
print template.render(lst=lst,c=c)
