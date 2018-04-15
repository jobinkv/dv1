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
form = cgi.FieldStorage()

# getlist() returns a list containing the
# values of the fields with the given name
#mod = form.getlist('m')
mod = form.getvalue('m')
if mod=='train':
	prind='Training'
if mod=='test':
	prind='Testing'
#for name in images:
#	print cgi.escape(name)
[imgs,labels]=readAnnotation(mod+'.txt')
llist = Counter(labels).keys()
#llist.sort()
#ipdb.set_trace()
lcount = Counter(labels).values()
#for name in images:
#	if cgi.escape(name) not in imgs_old:
#		cnt=cnt+1

slnos=list(np.arange(len(llist)))

'''To create the plot'''
objects = tuple(llist)
y_pos = np.arange(len(objects))
fig, ax = plt.subplots()
ax.barh(objects,y_pos, align='center')
thr = lambda l, t:  [v if (v <= t) else t for v in l ]
ax.barh(objects, thr(lcount,2000), align='center')
ax.barh(objects, thr(lcount,1000), align='center')
ax.barh(objects, thr(lcount,500), align='center')
ax.barh(objects, thr(lcount,100), align='center')
ax2 = ax.twinx()
ax2.set_ylim(ax.get_ylim())
ax2.set_yticks(range(len(objects)))
ax2.set_yticklabels(lcount)
ax.set_xticks([100,500,1000])
plt.title('Labels                                                                                    count')
plt.xlabel('')
plt.tight_layout()
plt.grid(True)
plt.savefig('statistics')
call(["cp", "statistics.png", "/home/jobinkv/Documents/r1/"])
call(["cp", "annotation.txt", "/home/jobinkv/Documents/r1/"])


templ = '''Content-type:text/html\r\n\r\n
 <html>
<head>
</head>
<body>
    <center>
<h3> {{prind}} images</h3>

<p>Statistics</p> 
        <table border="2" cellspacing="1">
 <caption>Table1: The showing the labels, the count of images and the link to view the images</caption>
	<tr>
	<td>Sl.No</td>
	<td>Labels</td>
	<td>No of training images</td>
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
		<a href="showLabeled.py?k={{lab}}&m=train">{{count}}</a>
		</td>
            </tr>
            {% endfor %}
	<tr><td></td><td>Total</td><td>{{total}}</td></tr>
        </table>
<figure>
  <img src="/r1/statistics.png" alt="">
<figcaption>Fig1. The bar plot showing the annotation statistics of each label.</figcaption>
</figure>
    </center>
    </body>
</html>'''
 
lst = zip(slnos,llist, lcount)
template = jinja2.Template(templ)
total=sum(lcount)
print template.render(lst=lst, total=total, prind=prind)
	
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
