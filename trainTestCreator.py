#!/usr/bin/python
import scipy.io as sio
import os
import numpy as np
import ipdb
import random 
from subprocess import call
SEED = 349
Max_Train_Imgs = 750
Max_Test_Imgs = 250

def chomp(x):
    if x.endswith("\r\n"): return x[:-2]
    if x.endswith("\n"): return x[:-1]
    return x

class annotationData:
        def __init__(self, row):
                self.img = row[0]
                self.label =chomp(row[1])

class labelCnt:
        def __init__(self, label):
                self.label = label
                self.cnt = 0

'''read the annotation file'''
def readAnnotation(file_name):
    list_annotation=[]
    with open(file_name, 'r') as data:
        x = []
        y = []
        for line in data:
            p = line.split('\t')
	    annotation = annotationData(p)
	    list_annotation.append(annotation)
    return list_annotation
def CrtLabelCnt(SelectedLabels):
	labelCnt_list=[]
	for label in selectedLabels:
		labePair = labelCnt(label)
		labelCnt_list.append(labePair)
	return labelCnt_list
def getLabelCnt(labelCnt,label):
	succses = 0
	inx=0
	for item in labelCnt:
		if item.label==label:
			succses=1
			return item.cnt,inx
			break
		inx=inx+1
	if succses==0:
		return -1,-1
selectedLabels=['3D objects','Scatter plot','Bar plots','Block diagram','Combined images','Confusion matrix','Flow chart','Graph plots','Heat map','Mask','Medical images','Natural images','Sketches','Tables']

labelCnt = CrtLabelCnt(selectedLabels)

annotationDatas = readAnnotation('/var/www/cgi-bin/v4/annotation.txt')

random.seed(SEED)
random.shuffle(annotationDatas)
call(["sed","-i", "/.png/d","./train.txt"])
call(["sed","-i", "/.png/d","./test.txt"])
train_file = open("train.txt","a")
test_file = open("test.txt","a")
for item in annotationDatas:
	[label_Cnt,labelInx] = getLabelCnt(labelCnt,item.label)
	if label_Cnt==-1:
		continue
	else:
		if label_Cnt<Max_Train_Imgs:
			train_file.write(item.img+'\t'+item.label+'\n')
			labelCnt[labelInx].cnt=labelCnt[labelInx].cnt+1
		elif label_Cnt<Max_Train_Imgs+Max_Test_Imgs:
			test_file.write(item.img+'\t'+item.label+'\n')
			labelCnt[labelInx].cnt=labelCnt[labelInx].cnt+1
train_file.close()
test_file.close()
print 'done!'
