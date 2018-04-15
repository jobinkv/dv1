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
def chomp(x):
    if x.endswith("\r\n"): return x[:-2]
    if x.endswith("\n"): return x[:-1]
    return x

class resData:
        def __init__(self, row):
                self.img = row[0]
                self.label =chomp(row[1])
                self.pred  =chomp(row[2])
def readData(file_name):
    list_data=[]
    with open(file_name, 'r') as data:
        for line in data:
            p = line.split('\t')
	    annotation = resData(p)
	    list_data.append(annotation)
    return list_data
#for name in images:
#	print cgi.escape(name)
#for name in images:
#	if cgi.escape(name) not in imgs_old:
#		cnt=cnt+1
def get_unique_list(lst):
        if isinstance(lst,list):
            return list(set(lst))
def getLabels(testData):
	out=[]
	for item in testData:
		out.append(item.label)
	return get_unique_list(out)
def findImgs(testData,tru_label,pred_label):
	out=[]
	for item in testData:
		if item.label==tru_label and item.pred==pred_label:
			out.append(item.img)
	return out

form = cgi.FieldStorage()
# getlist() returns a list containing the
pred_label = form.getvalue('p')
tru_label = form.getvalue('l')
feature = form.getvalue('f')
testData=readData(feature+'.txt')

#pred_label ='Graph plots'
#tru_label='Natural images'
imgss = findImgs(testData,tru_label,pred_label)
#for item in labels:
#	print '\n'
#	for pred in labels:
#		print len(findImgs(testData,item,pred)),'\t'

#ipdb.set_trace()




 
#lst = zip(slnos,llist, lcount)
#template = jinja2.Template(templ)
#total=sum(lcount)
#print template.render(labels=labels,testData=testData,findImgs=findImgs)
	
print "Content-Type: text/html\n"
print '<html><body><center>'
if pred_label!=tru_label:
	print '<h3>The images with true label '+tru_label+' miss classified as '+pred_label+' </h3>'
else:
	print '<h3>The currectly classified images with label '+pred_label+'</h3>'
print '<p><a href="cv1.py?f='+feature+'">back to confusion matrix</a></p>'
print '<table border="2" cellspacing="1">'
print '<tr><td>Sl No</td><td>Image</td>'
cnt=1
for item in imgss:
	print '<tr><td>'+str(cnt)+'</td><td><img src="/pdfFig2/subImg/'+item+'"> \
	<figcaption>Image name: '+item+'</figcaption></td></tr>'
	cnt=cnt+1
print '<tr><td>.</td><td><a href="cv1.py?f='+feature+'">back to confusion matrix</a></td></tr>'
print '</table></center>'
print '</body></html>'
		


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
