#!/usr/bin/python 
# -*- coding: utf-8 -*-

import datetime
def convertDateFormat(date):
#    print(date,date[3:5],date[0:2],date[6:10]) #start and stop indices, not start, length indices
    day=int(date[3:5])
    month=int(date[0:2])
    year=int(date[6:10])
    dt=datetime.date(year,month,day) 
    return dt.strftime("%Y-%m-%d")


import csv 
def WriteXMLHeader():
    output=open("XMLoutput.txt","w") #first open in write mode to overwrite prev stuff
    output.write("<markers>\n")
    output.close()
def WriteXMLFooter():
    output=open("XMLoutput.txt","a") #then append mode
    output.write("</markers>")
    output.close()

def WriteXML():
    import locale
    locale.setlocale(locale.LC_ALL, '')
#    data=csv.reader(open('output.txt'))
    data=csv.reader(open('output_geocoded.txt'))
    xmldata=""
    for row in data:
#date,casenumber,address(city used to be separate),zipcode,appraisal,minbid,status,lat,lng
#zip,appraisal,minbid,status,lat,lng used to be bumped out one due to addition of city
        if row[4]=="":
            appraisal=0.0
        else:
            appraisal=float(row[4])
        if row[5]=="":
            minbid=str(0.0)
        else:
            minbid=str(locale.currency(float(row[5]), grouping=True))
        if row[3]=="":
            zipcode=0
        else:
            if row[3][0:2]=="OH":
                if len(row[3])>7:
                    zipcode=int(row[3][3:])
                else:
                    zipcode=0
            else:
                zipcode=int(row[3])
            date=convertDateFormat(row[0])
#HTML must be escaped in XML. ie. <br> --> &lt;br&gt; this prevents XML from complaining that poor formed document
#must have some sort of header/footer as I do here otherwise get "junk after...."
        xmldata+="<marker lat=\""+row[7]+"\" lng=\""+str(row[8])+"\" html=\""+date+" &lt;br&gt; "+row[1]+" &lt;br&gt; "+minbid+"\" label=\""+row[2]+" "+minbid+"\"/>\n" #format similar to
#        xmldata+="{ \"title\": \""+row[2]+"\", \"lat\": "+row[8]+", \"lng\":"+row[9]+", \"description\":\""+row[0]+" "+row[1]+" "+row[2]+" "+row[6]+"\" },\n" #for svennerberg.com multiple-markers example
        #print(xmldata)
    output=open("XMLoutput.txt","a")
    output.write(xmldata)
    output.close()

#def formatLine():



import sys
WriteXMLHeader()
WriteXML()
WriteXMLFooter()


