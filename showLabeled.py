#!/usr/bin/python
import scipy.io as sio
import os
import numpy as np
import cgi, cgitb 
import jinja2
import ipdb
'''read the annotation file'''
def readAnnotation(file_name,key):
    with open(file_name, 'r') as data:
        x = []
        for line in data:
            p = line.split('\t')
            if key==p[1].split('\n')[0]:
               x.append(p[0])
    return x


#ipdb.set_trace()
#[imgs,labels]=readAnnotation('annotation.txt')
'''Input of the system'''

# Create instance of FieldStorage 
form = cgi.FieldStorage() 
# Get data from fields
key = form.getvalue('k')
mod = form.getvalue('m')
Imagelist=readAnnotation(mod+'.txt',key)
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
	<tr>
<td>Sl.No</td>
<td>Automatically choosen Images</td>
</tr>
	
        {% for slno, img in lst %}
            <tr>
                <td>
		{{slno+1}} 
                </td>
                <td>
		<img src="/pdfFig2/subImg/{{img}}">
		<figcaption>Image name: {{img}}</figcaption>
                </td>
            </tr>
            {% endfor %}
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
