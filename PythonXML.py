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
    output=open("XMLoutput.txt","w")
    output.write("<markers>\n")
    output.close()
def WriteXMLFooter():
    output=open("XMLoutput.txt","a")
    output.write("</markers>")
    output.close()

def WriteXML():
#    data=csv.reader(open('output.txt'))
    data=csv.reader(open('output_geocoded.txt'))
    xmldata=""
    for row in data:
        if row[5]=="":
            appraisal=0.0
        else:
            appraisal=float(row[5])
        if row[6]=="":
            minbid=0.0
        else:
            minbid=float(row[6])
        if row[4]=="":
            zipcode=0
        else:
            if row[4][0:2]=="OH":
                if len(row[4])>7:
                    zipcode=int(row[4][3:])
                else:
                    zipcode=0
            else:
                zipcode=int(row[4])
            date=convertDateFormat(row[0])
        xmldata+="<marker lat=\""+row[8]+"\" lng=\""+row[9]+"\" html=\""+row[0]+" "+row[1]+" "+row[2]+" "+row[6]+"\" label=\""+row[2]+" "+row[6]+"\"/>\n"
    output=open("XMLoutput.txt","a")
    output.write(xmldata)
    output.close()

#def formatLine():



import sys
WriteXMLHeader()
WriteXML()
WriteXMLFooter()


