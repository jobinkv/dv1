#!/usr/bin/python
import scipy.io as sio
import os
import numpy as np
import cgi, cgitb 
import jinja2
import ipdb
import csv 
'''read the annotation file'''
def readAnnotation(file_name,key):
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
csvred = readClassification('machineannotationV4.txt')
sortedlist = sorted(csvred, key=lambda row: row[int(key)], reverse=True)
Imagelist=[]
cnt=0
for row in sortedlist:
	Imagelist.append(row[0])
	cnt=cnt+1
	if cnt==300:
		break
#	print row[0]
#ipdb.set_trace()
#Imagelist=readAnnotation('annotation.txt',key)
#for itm in Imagelist:
#	print "<h3>The query image name %s</h3>" % (itm)
	#print itm

#print "</body>"
#print "</html>"
templ = '''Content-type:text/html\r\n\r\n
 <html>
<head>
</head>
<body> 
    <center>
        <table border="2" cellspacing="1">
<form action="./procesMain.py" method="post">
	<tr><td>Sl.No</td><td>Automatically choosen Images</td><td>Select a label 
</td>
<td>
Iterate
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
  <input type="checkbox" style="zoom:3" name="id" value={{img}} checked><br>
		</td>
		<td>
		<a href="main.py?v={{img}}">Iterate</a>
		</td>
            </tr>
            {% endfor %}
	<tr><td>End</td><td>Please submit your changes</td><td><input type="submit" style="zoom:3" value="Submit"></td> </tr>
	</form>
        </table>
    </center>
    </body>
</html>'''

slnos=list(np.arange(len(Imagelist)))
#let = ["2010_05539963-Figure1-1subFig-4.png", '2010_05539963-Figure1-1subFig-4.png', '2010_05539963-Figure1-1subFig-4.png', '2010_05539963-Figure1-1subFig-4.png']

lst = zip(slnos,Imagelist)
template = jinja2.Template(templ)
print template.render(lst=lst)
