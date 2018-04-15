#!/usr/bin/python
import scipy.io as sio
import os
import numpy as np
import cgi, cgitb 
import jinja2
from collections import Counter
import ipdb
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
#import pylab
from subprocess import call
import json


'''
def readAnnotation(file_name):
    with open(file_name, 'r') as data:
        x = []
        y = []
        for line in data:
            p = line.split('\t')
            x.append(p[0])
            y.append(p[1])
    return x, y
form = cgi.FieldStorage()

# getlist() returns a list containing the
# values of the fields with the given name
images = form.getlist('id')
#label = form.getlist('label')
#for name in images:
#	print cgi.escape(name)
[imgs_old,labels_old]=readAnnotation('annotation.txt')
file = open("annotation.txt","a") 
cnt=0
for name in images:
	if cgi.escape(name)!='none':
		if cgi.escape(name).split('@')[0] not in imgs_old:
			file.write(cgi.escape(name).split('@')[0]+'\t'+cgi.escape(name).split('@')[1]+'\n') 
			cnt=cnt+1
file.close()
[imgs,labels]=readAnnotation('annotation.txt')
llist = Counter(labels).keys()
#llist.sort()
#ipdb.set_trace()
lcount = Counter(labels).values()
#for name in images:
#	if cgi.escape(name) not in imgs_old:
#		cnt=cnt+1

slnos=list(np.arange(len(llist)))

objects = tuple(llist)
y_pos = np.arange(len(objects))
plt.barh(y_pos, lcount, align='center', alpha=0.5)
plt.yticks(y_pos, objects)
plt.xlabel('Count')
plt.title('Sub-figure labels')
plt.tight_layout()
plt.grid(True)
plt.savefig('statistics')
call(["cp", "statistics.png", "/home/jobinkv/Documents/r1/"])
call(["cp", "annotation.txt", "/home/jobinkv/Documents/r1/"])
'''

templ = '''Content-type:text/html\r\n\r\n
 <html>
<head>
</head>
<body>
    <center>
<h3> No of newly added images: {{cnt}}</h3>
<p>Annotation statistics</p> 
        <table border="2" cellspacing="1">
	<tr>
	<td>Sl.No</td>
	<td>Labels</td>
	<td>Description</td>
	</tr>
        {% for slno, lab, count in lst %}
            <tr>
                <td>
		{{slno+1}} 
                </td>
                <td>
		{{lab}}
                </td>
		<td>
		{{count}}
		</td>
            </tr>
            {% endfor %}
        </table>
    </center>
    </body>
</html>'''

llist=['a','b']
lcount = [10, 12]
slnos=list(np.arange(len(llist)))
 
lst = zip(slnos,llist, lcount)
template = jinja2.Template(templ)
#total=sum(lcount)
print template.render(lst=lst)
	
#print "Content-Type: text/html\n"
#print '<html><body>'
#cnt=0
#for name in images:
#	if cgi.escape(name)!='none':
#		print '<p>'+cgi.escape(name)+'</p>'
#		print '<p>'+cgi.escape(name).split('@')[0]+'</p>'
#		print '<p>'+cgi.escape(name).split('@')[1]+'</p>'
#print 'Selected label:', label[0]
#cnt=0
#for name in images:
#	if cgi.escape(name) not in imgs:
#		cnt=cnt+1
#print '<p>Number of newly added image:',cnt, '</p>'
#print '<p><a href="/pdfFig2/subfigureLabelCreator/">Pic a quary image</a></p>'
#print '</body></html>'
