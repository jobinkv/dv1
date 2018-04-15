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
def labelAccuracy(testData,tru_label):
	total=0
	correct=0
	for item in testData:
		if item.label==tru_label:
			total=total+1
		if item.label==tru_label and item.pred==tru_label:
			correct=correct+1
	return correct*10000/total

form = cgi.FieldStorage()
mode = form.getvalue('f')
#mode='rcnn'
testData=readData(mode+'.txt')
if mode=='rcnn':
	feat='FC-CNN'
elif mode=='dcnn':
	feat='FV-CNN'
elif mode=='drcnn':
	feat='FV-CNN+FC-CNN'
else:
	feat='un-known'
labels = getLabels(testData)
labels.sort()
cnt=0
for item in testData:
	if item.label==item.pred:
		cnt=cnt+1
accuracy = cnt*10000/len(testData)


	
print "Content-Type: text/html\n"
print '<html><body><center>'
print '<br>'
print '<br>'
print '<br>'
print '<br>'
print '<h3>Selected feature '+feat+'</h3>'
print '<h3>Classification acccuracy = No of correctly classified/Total test sample</h3>'
print '<h3>      ='+str(cnt)+'/'+str(len(testData))+' = '+str(float(accuracy)/100)+'%</h3>'
print '<h3>The confusion metrics</h3>'
print '<p>To view the images, click on the corresponging cell</p>'
print '<table border="1" cellspacing="1">'
print '<tr><td>Predicted labels <br> True label</td>'
for item in labels:
	print '<td>'+item+'</td>'
print '<td>Label wise accuracy</td>'
print '</tr>'
for label in labels:
	print '<tr><td>'+label+'</td>'
	for pred in labels:
		print '<td><form action="si.py" method="get"><input type="hidden" \
		name="l" value="'+label+'" checked><input type="hidden" name="p" \
		value="'+pred+'" checked><input type="hidden" \
                name="f" value="'+mode+'" checked><input type="submit" value="'+str(len(findImgs(testData,label,pred)))+'\
		"></form></td>'
	print '<td>'+str(float(labelAccuracy(testData,label)/100))+'%</td>'
	print '</tr>'
		
print '</center></body></html>'


