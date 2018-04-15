#!/usr/bin/python
import scipy.io as sio
import os
import numpy as np
import cgi, cgitb 
import jinja2
import ipdb
'''fin out the index of a given image name'''
def findQueryId(figNames,query):
	[tem1,NofImages] = figNames.shape
	out=-1
	for i in range(0,NofImages):
		if figNames[0,i]==query:
			out = i
	return out
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
'''Read data and cookies'''
def readDataset(file_name):
    with open(file_name, 'r') as data:
        x = []
        for line in data:
            p = line.split('\t')
            x.append(p[0])
    return x
'''find the list of images similar to the query image'''
def getSimilarImageList(mat_contents,NofTopretrival,queryName):
	similarityMetrix = mat_contents['data']['similarityMatrix'][0,0]
	#ipdb.set_trace()
	figNames = mat_contents['data']['figNames'][0,0]
	PyqueryId = findQueryId(figNames,queryName)
	if PyqueryId>=0:
		quaryArray = similarityMetrix[PyqueryId,:]
	else:
		print 'The given query image '+queryName+' is not in the database'
		exit()
	quaryAA = np.absolute(quaryArray) #query absolute array
	sortedIndices = np.argsort(quaryAA)
	outImagelist=[]

	[imgs,labels]=readAnnotation('annotation.txt')
	b=0
	for i in range(0, NofTopretrival*5):   # sortedIndices:
		ids= sortedIndices[i]
		fileName = str(figNames[0,ids][0])
		if fileName not in imgs:
			outImagelist.append(fileName)
			b=b+1
		if b == NofTopretrival:
			break		
	return outImagelist


#ipdb.set_trace()
#[imgs,labels]=readAnnotation('annotation.txt')
'''Input of the system'''
#ipdb.set_trace()
query_name = '2015_07298747-Figure1-1subFig-2.png'
NofTopretrival = 20
#mat_contents = sio.loadmat('/home/jobinkv/Documents/pdfFig2/CreateLabelCaterories/dcnn/data.mat')
# Create instance of FieldStorage 
form = cgi.FieldStorage() 
# Get data from fields
query_name = form.getvalue('v')
c=form.getvalue('c')

mat_contents = sio.loadmat('/home/jobinkv/similarityData/'+query_name.split('_')[0]+'/data.mat')
Imagelist=getSimilarImageList(mat_contents,NofTopretrival,query_name)
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
<form action="./s3.py" method="post">
	<tr><td>Sl.No</td><td>Automatically choosen Images</td><td>
<a href="main.py?v={{query_name}}&c=Y">tic all</a>
</td><td>Iterate</td></tr>
	
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
  <input type="checkbox" style="zoom:3" name="id" value={{img}} {{checked}}><br>
		</td>
		<td>
		<a href="main.py?v={{img}}">Iterate</a>
		</td>
            </tr>
            {% endfor %}
	<tr><td>End</td><td>
Select a label 
<select style="zoom:2" name="label">
<option value="slick">slick</option>
<option value="Flower">Flower</option>
<option value="Medical images">Medical images</option>
<option value="vehicle">vehicle</option>
<option value="segment">segment</option>
<option value="bird">bird</option>
<option value="tsne plot">tsne plot</option>
<option value="3d object">3d object</option>
<option value="3d graph">3d graph</option>
<option value="buiding">buiding</option>
<option value="human">human</option>
<option value="3d bar graph">3d bar graph</option>
<option value="box plot">box plot</option>
<option value="pointgraph">pointgraph</option>
<option value="outdoor">outdoor</option>
<option value="Indoor">Indoor</option>
<option value="face">face</option>
<option value="xygraph">xygraph</option>
<option value="Block diagram">Block diagram</option>
<option value="Graph">Graph</option>
<option value="Bar graph">Bar graph</option>
<option value="Pie-chart">Pie-chart</option>
<option value="Sketches">Sketches</option>
<option value="Photograph">Photograph</option>
<option value="Photograph with markings">Photograph with markings</option>
<option value="flow chart">flow chart</option>
<option value="Heat map">Heat map</option>
<option value="Mask">Mask</option>
<option value="Confusion Matrix">Confusion Matrix</option>
</select>
</td><td><input type="submit" style="zoom:3" value="Submit"></td> </tr>
	</form>
        </table>
    </center>
    </body>
</html>'''

slnos=list(np.arange(len(Imagelist)))
#let = ["2010_05539963-Figure1-1subFig-4.png", '2010_05539963-Figure1-1subFig-4.png', '2010_05539963-Figure1-1subFig-4.png', '2010_05539963-Figure1-1subFig-4.png']

lst = zip(slnos,Imagelist)
template = jinja2.Template(templ)
if c=='Y':
	checked=' '
else:
	checked='checked'
print template.render(lst=lst,checked=checked,query_name=query_name)
