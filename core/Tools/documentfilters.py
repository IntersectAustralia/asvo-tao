import re,os,sys
import StringIO
import os, shlex, subprocess,string
import logging
import locale
import plot_filter

if __name__ == '__main__':
	InputFilePath=sys.argv[1] # CSV File
	InputFile = open(InputFilePath, 'r')
	OutputFile=open('Insert.sql','w') 
	
	SQLStmt="INSERT INTO tao_bandpassfilter('label','filter_id','description')	VALUES ('{0}','{1}','{2} <p>Additional Details: <a href=\"../static/docs/bpfilters/{3}.html\">{4}</a>.</p>');"
	
	DataLines=InputFile.readlines()
	
	for Line in DataLines:    
		DataFields=Line.rstrip().split(",")
		
		FileName=DataFields[0].split("/")[1]
		plot_filter.plot_filter(DataFields[0],"skymapper/"+FileName+".png")
		RSTFileName=FileName+".rst"
		RSTFile = open("skymapper/"+RSTFileName, 'w')
		RSTStr="""
{0}
=========
.. raw:: html

\t<p>
\t{1}  
\t</p>
.. image:: spectra/{2}.png
"""
		
		RSTFile.write(RSTStr.format(DataFields[1],DataFields[2],FileName))
		RSTFile.close() 
		OutputFile.write(SQLStmt.format(DataFields[1],DataFields[0],DataFields[2],FileName,DataFields[1])+"\n")
		
	InputFile.close() 