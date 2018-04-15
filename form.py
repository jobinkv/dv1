#!/usr/bin/python
import scipy.io as sio
import os
import numpy as np
import cgi, cgitb 
import jinja2
import ipdb
import random


templ1 = '''Content-type:text/html\r\n\r\n
<html>
<head>
<style> 
input[type=text] {
    width: 10%;
    padding: 12px 20px;
    margin: 8px 0;
    box-sizing: border-box;
}
select {
    width: 10%;
    padding: 16px 20px;
    border: none;
    border-radius: 4px;
    background-color: lightblue;
}
input[type=text]:focus {
    background-color: lightblue;
}
input[type=button], input[type=submit], input[type=reset] {
    background-color: lightblue;
    border: none;
    color: black;
    padding: 16px 32px;
    text-decoration: none;
    margin: 4px 2px;
    cursor: pointer;
}
</style>
</head>
<body>
<center>
<br>
<br>
<br>
<br>
<form align="center" action="s2p2.py">
	Select a cluster :    <select name="k">
<option value="1">
3D objects
</option>
<option value="2">
Bar plots
</option>
<option value="3">
Block diagram
</option>
<option value="4">
Box plot
</option>
<option value="5">
Combined images
</option>
<option value="6">
Combined plots
</option>
<option value="7">
Confusion matrix
</option>
<option value="8">
Flow chart
</option>
<option value="9">
Graph plots
</option>
<option value="10">
Heat map
</option>
<option value="11">
Histogram
</option>
<option value="12">
Mask
</option>
<option value="13">
Medical images
</option>
<option value="14">
Natural images
</option>
<option value="15">
Pie chart
</option>
<option value="16">
Polar plot
</option>
<option value="17">
Scatter plot
</option>
<option value="18">
Sketches
</option>
<option value="19">
Tables
</option>
<option value="20">
Vector plot
</option>
</select> <br>
  Staring point : <input type="text" name="sp" value="0">
  <br>
  Number of images :<input type="text" name="ni" value="100">
  <br>
<br>
<br>
  <input type="submit" value="Show me the images">
</form> 

</center>
</body>
</html>


'''

templ2 = '''Content-type:text/html\r\n\r\n
<html>
<head>
<style> 
input[type=text] {
    width: 10%;
    padding: 12px 20px;
    margin: 8px 0;
    box-sizing: border-box;
}
select {
    width: 10%;
    padding: 16px 20px;
    border: none;
    border-radius: 4px;
    background-color: lightblue;
}
input[type=text]:focus {
    background-color: lightblue;
}
input[type=button], input[type=submit], input[type=reset] {
    background-color: lightblue;
    border: none;
    color: black;
    padding: 16px 32px;
    text-decoration: none;
    margin: 4px 2px;
    cursor: pointer;
}
</style>
</head>
<body>
<center>
<br>
<br>
<br>
<br>
<form align="center" action="s2p1.py">
	Select a cluster :    <select name="k">
<option value="1">
3D objects
</option>
<option value="2">
Bar plots
</option>
<option value="3">
Block diagram
</option>
<option value="4">
Box plot
</option>
<option value="5">
Combined images
</option>
<option value="6">
Combined plots
</option>
<option value="7">
Confusion matrix
</option>
<option value="8">
Flow chart
</option>
<option value="9">
Graph plots
</option>
<option value="10">
Heat map
</option>
<option value="11">
Histogram
</option>
<option value="12">
Mask
</option>
<option value="13">
Medical images
</option>
<option value="14">
Natural images
</option>
<option value="15">
Pie chart
</option>
<option value="16">
Polar plot
</option>
<option value="17">
Scatter plot
</option>
<option value="18">
Sketches
</option>
<option value="19">
Tables
</option>
<option value="20">
Vector plot
</option>
</select> <br>
  Staring point : <input type="text" name="sp" value="0">
  <br>
  Number of images :<input type="text" name="ni" value="100">
  <br>
   Check mark :	<select name="c">
<option value="1">Yes</option>
<option value="0">No</option>
</select> <br>
<br>
<br>
  <input type="submit" value="Show me the images">
</form> 

</center>
</body>
</html>'''

form = cgi.FieldStorage() 
ticmark = int(form.getvalue('c'))
if ticmark==1:
	template = jinja2.Template(templ1)
else:
	template = jinja2.Template(templ2)
print template.render()
