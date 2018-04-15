#!/usr/bin/python
import scipy.io as sio
import os
import numpy as np
import cgi, cgitb 
import jinja2
import ipdb
import csv 
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
 #<input type="checkbox" style="zoom:3" name="id" value={{img}} {{c}}><br>
#print "</body>"
#print "</html>"
templ = '''Content-type:text/html\r\n\r\n
 <html>
<head>
</head>
<body> 
    <center>
        <table border="2" cellspacing="1">
<form action="s3v1.py" method="get">
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
		<select style="zoom:1" name="id">
<option value="none">none</option>
<option value="{{img}}@Sketches">Sketches</option>
<option value="{{img}}@Block diagram">Block diagram</option>
<option value="{{img}}@Combined images">Combined images</option>
<option value="{{img}}@Mask">Mask</option>
<option value="{{img}}@Heat map">Heat map</option>
<option value="{{img}}@Pie chart">Pie chart</option>
<option value="{{img}}@Tables">Tables</option>
<option value="{{img}}@Combined plots">Combined plots</option>
<option value="{{img}}@Bar plots">Bar plots</option>
<option value="{{img}}@Algorithm">Algorithm</option>
<option value="{{img}}@Flow chart">Flow chart</option>
<option value="{{img}}@Scatter plot">Scatter plot</option>
<option value="{{img}}@Graph plots">Graph plots</option>
<option value="{{img}}@Confusion matrix">Confusion matrix</option>
<option value="{{img}}@3D objects">3D objects</option>
<option value="{{img}}@Synthetic image">Synthetic image</option>
<option value="{{img}}@Processed image">Processed image</option>
<option value="{{img}}@Medical images">Medical images</option>
<option value="{{img}}@Natural images">Natural images</option>
<option value="{{img}}@Nyquist plot">Nyquist plot</option>
<option value="{{img}}@Box plot">Box plot</option>
<option value="{{img}}@Vector plot">Vector plot</option>
<option value="{{img}}@Polar plot">Polar plot</option>
<option value="{{img}}@Histogram">Histogram</option>
<option value="{{img}}@Customised graph">Customised graph</option>
</select>
		</td>
            </tr>
            {% endfor %}
	<tr><td>End</td>
	<td>
<select style="zoom:2" name="label">
<option value="nill">.</option>
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
lst = zip(slnos,Imagelist)
template = jinja2.Template(templ)
print template.render(lst=lst)
