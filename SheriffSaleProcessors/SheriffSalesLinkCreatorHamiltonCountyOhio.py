#this program takes as input a saved search from the Franklin County Sheriff sales site
#the input should be the detailed view listing of properties

import re
def translatetownship(name):
    translatelist={"ADDYSTON":"Addyston",
        "AMBERLEY VILLAGE":"Amberley Village",
        "ANDERSON TWSP":"Anderson Township",
        "ARLINGTON HGTS":"Arlington Heights",
        "BLUE ASH":"Blue Ash",
        "CHEVIOT":"Cheviot",
        "CINTI":"Cincinnati",
        "CINCI":"Cincinnati",
        "CINC":"Cincinnati",
        "CLEVES":"Cleve",
        "COLERAIN TWSP":"Colerain Township",
        "COLLEGE HILL":"College Hill",
        "COLUMBIA TWSP":"Columbia Township",
        "CROSBY TWSP":"Crosby Township",
        "DEER PARK":"Deer Park",
        "DELHI TWSP":"Delhi Township",
        "ELMWOOD PL":"Elmwood Place",
        "EVENDALE":"Evendale",
        "FAIRFAX":"Fairfax",
        "FOREST PARK":"Forest Park",
        "GLENDALE":"Glendale",
        "GOLF MANOR":"Golf Manor",
        "GREEN":"Green",
        "GREEN TWSP":"Green Township",
        "GREENHILLS":"Greenhills",
        "HARRISON":"Harrison",
        "INDIAN HILL":"Indian Hill",
        "LINCOLN HGTS":"Lincoln Heights",
        "LOCKLAND":"Lockland",
        "LOVELAND":"Loveland",
        "MADEIRA":"Madeira",
        "MADERIA":"Maderia",
        "MARIEMONT":"Mariemont",
        "MIAMI TWSP":"Miami Township",
        "MONTGOMERY":"Montgomery",
        "MT HEALTHY":"Mount Healthy",
        "N C H":"North College Hill",
        "NCH":"North College Hill",
        "NEWTOWN":"Newtown",
        "NORTH BEND":"North Bend",
        "NORWOOD":"Norwood",
        "READING":"Reading",
        "SHARONVILLE":"Sharonville",
        "SILVERTON":"Silverton",
        "SPRINGDALE":"Springdale",
        "SPRINGFIELD TWSP":"Springfield Township",
        "ST BERNARD":"St Bernard",
        "SYCAMORE TWSP":"Sycamore Township",
        "SYMMES TWSP":"Symmes Township",
        "TERRACE PARK":"Terrace Park",
        "WHITEWATER TWSP":"Whitewater Township",
        "WOODLAWN":"Woodlawn",
                   "WYOMING":"Wyoming",
                   "NONE":"Cincinnati"
}
#    grep option HamiltonCtyOhio05142012ExecPropertySales.aspx.html | sed 's/<[^>]*>/"/;s/<[^>]*>/":"",/;'
    return translatelist[name]

def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)
def striptdfontend(data):
    p = re.compile(r'</font></td>')
    return p.sub('', data)
def striptdend(data):
    p = re.compile(r'</td>')
    return p.sub('', data)
def stripnowrap(data):
    p = re.compile(r' nowrap="nowrap"')
    return p.sub('',data)
def stripspaces(data):
    p = re.compile(r' ')
    return p.sub('+',data)
def stripampersand(data):
    p = re.compile(r'&amp;')
    return p.sub('and',data) # &amp 
def stripcomma(data):
    p = re.compile(r',')
    return p.sub(' ',data)
def prepprice(data):
    temp=striphtml(data.rstrip())
    temp2=temp.strip() #remove whitespace
    p = re.compile(r'\$') #remove $, its spec in regex so need to escape it
    temp3=p.sub('',temp2)
    p = re.compile(r',') #remove comma in price since that'll screw things up as far as outputting to csv.
    return p.sub('',temp3)


def InsertSaleInfoIntoDB(date,CaseNumber,Address, Plaintiff,Defendant,Attorney,SoldTo,PID,Zipcode,Appraisal,MinBidAmt,SaleAmt,SaleStatus):
    con = mdb.connect('localhost', 'nicolae', 'ceausescu', 'SheriffSales')
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute("INSERT INTO Property(SaleDate,CaseNumber,Address,Appraisal,SaleStatus,Attorney,Defendant,Plaintiff,SaleAmt) VALUES ( %s,%s,%s,%s,%s,%s,%s,%s,%s)", (date, CaseNumber,Address,Appraisal,SaleStatus,Attorney,Defendant,Plaintiff,SaleAmt)) #even though their database types are int/float etc they are entered as strings here.... 

    con.commit()
    cur.close()
    con.close()  


def InsertIntoDB(date,CaseNumber,Address, Plaintiff,Defendant,Attorney,SoldTo,PID,Zipcode,Appraisal,MinBidAmt,SaleAmt,SaleStatus):
    con = mdb.connect('localhost', 'nicolae', 'ceausescu', 'SheriffSales')
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute("INSERT INTO Property(SaleDate,CaseNumber,Address,Appraisal,SaleStatus,Attorney,Defendant,Plaintiff) VALUES ( %s,%s,%s,%s,%s,%s,%s,%s)", (date, CaseNumber,Address,Appraisal,SaleStatus,Attorney,Defendant,Plaintiff)) #even though their database types are int/float etc they are entered as strings here.... 
    con.commit()
    cur.close()
    con.close()  



def QueryDatabaseIfRecordExists(date,CaseNumber,Address, Plaintiff,Defendant,Attorney,SoldTo,PID,Zipcode,Appraisal,MinBidAmt,SaleAmt,SaleStatus):
    key=-1 #primary keys aren't negative as far as I know. This is the sentinel value
    con = mdb.connect('localhost', 'nicolae', 'ceausescu', 'SheriffSales')
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
# check to see if record exists before inserting, if exists check for salestatus change, update saleamt 
        resultcount=int(cur.execute("SELECT * FROM Property WHERE SaleDate=%s and CaseNumber=%s and Address=%s and Appraisal=%s and PID=%s ", (date, CaseNumber,Address,Appraisal,PID)))  # look for match on all fields except those that would've been update after teh property was sold

        if resultcount==1:
            row=cur.fetchone()
            key=int(row['id'])
        elif resultcount>1:
            print("multiple results:%i",resultcount)
            key=-2
            #rows=cur.fetchall()
 #       else:
 #           print("no results found"),
#            print("SELECT * FROM Property WHERE SaleDate=%s and CaseNumber=%s and Address=%s and Appraisal=%s and PID=%s " % (date, CaseNumber,Address,Appraisal,PID))  
    cur.close()
    con.close()  
    return int(key) #otherwise it is a long
    

def ProcessFile(inputfilename,outputfilename):
    print("Using input:%s and output:%s" % (inputfilename,outputfilename))
    AuctionListFile=open(inputfilename,'r')
    linecounter=0
    propertyRecordcounter=0
    SaleDate=""
    CaseNumber=""
    Plaintiff=""
    Defendant=""
    Attorney=""
    PID="" #parcel ID?
    SoldTo=""
    SaleStatus=""
    SaleAmt=""
    Address=""
    Zipcode=""
    Appraisal=""
    MinBidAmt=""
    SaleStatus=""
    enddataflag=0
    data=""
#create property record object. initialize with these extracted values
#geocode Property Record, check if record present. update with new data (sold info->soldto,saleprice)

#although keying off line # works, it isn't foolproof. yet there aren't tags to truly key off of either. 

#Hamilton Cty Data:
#headers on line 210
#records start on line 211
    for line in AuctionListFile:

        if (linecounter > 210) and (enddataflag==0): 
#            print(line) 
            line1=line.strip()
            linelower=line.lower()
            #data rows have td in them.
            if line.find("<td>")!=-1:
                parseddata=ParseTableData1(line.strip())
                #print(parseddata)
#2H['<td>A1307095', 'J P MORGAN CHASE BANK', 'AHERN, STEPHANIE', '6740 PARKLAND AVE', 'DENNIS REIMER', '440-600-5500', '$60,000', '$40,000', 'CINTI', 0, '3/27/2014</td>'
                CaseNumber=parseddata[0][4:] #remove <td> at front
                Plaintiff=parseddata[1]
                Defendant=parseddata[2]
                Address=parseddata[3]+" "+translatetownship(parseddata[8])+" Ohio"
                Attorney=parseddata[4]
                Appraisal=prepprice(parseddata[6])
                MinBidAmt=prepprice(parseddata[7])
                SaleDate=convertDateFormatDMYSlashdelimited(parseddata[10][0:-5]) #remove </td> at end.
                SaleStatus=parseddata[9]
                #print(CaseNumber,Plaintiff,Defendant,Address,Attorney,Appraisal,MinBidAmt,SaleDate,SaleStatus)
                if 1==1:
                    #print(CaseNumber,Plaintiff,Defendant,Address,Attorney,appraisal,minbidamt,SaleDate)
                    key=QueryDatabaseIfRecordExists(SaleDate,CaseNumber,Address, Plaintiff,Defendant,Attorney,SoldTo,PID,Zipcode,Appraisal,MinBidAmt,SaleAmt,SaleStatus) 
                    #key=99
                    if key==-1: # no results found, enter into database
                        print("-"),
                        InsertIntoDB(SaleDate,CaseNumber,Address, Plaintiff,Defendant,Attorney,SoldTo,PID,Zipcode,Appraisal,MinBidAmt,SaleAmt,SaleStatus)
                    elif key==-2:
                        print("uhoh multiple results returned")
                    elif key==-3:
                        print(","), #record is unchanged, don't do anything
                    else:
                        print("+"), #record has changed and we are updating it using the key
                        #we DONT want to update Franklin county records as that destroys what the appraisal amount was. As when a property is past its sale date then the appraisal value is replaced with $0.00

            if line.find("</table>")!=-1: #this signals the end of the property list                                                              
                enddataflag=1
        else:
            linecounter+=1
    output=open(outputfilename,"w")
    output.write(data)
    output.close()

def ProcessSalesFile(inputfilename,outputfilename):
    print("Processing a SALES file.!!")
    print("Using input:%s and output:%s" % (inputfilename,outputfilename))
    AuctionListFile=open(inputfilename,'r')
    linecounter=0
    propertyRecordcounter=0
    SaleDate=""
    CaseNumber=""
    Plaintiff=""
    Defendant=""
    Attorney=""
    PID="" #parcel ID?
    SoldTo=""
    SaleStatus=""
    SaleAmt=""
    Address=""
    Zipcode=""
    Appraisal=""
    MinBidAmt=""
    SaleStatus=""
    enddataflag=0
    data=""

#although keying off line # works, it isn't foolproof. yet there aren't tags to truly key off of either. 

#Hamilton Cty Data:
#headers on line 215
#records start on line 217
    for line in AuctionListFile:
        if (linecounter > 216) and (enddataflag==0): #first valid record starts on line 150 in the detailed view
            line1=line.strip()
            linelower=line.lower()
#could simply go off of line that we are on as 1st line holds most property data, 2nd line states whether property still for sale, 3rd,4th are formatting
            if line.find("<td><font face=\"Trebuchet MS\" size=\"2\">")!=-1:
                parseddata=ParseTableData1(line.strip())
#                print(parseddata)
                propertyRecordcounter=0
            SaleStatus="SOLD"
                
            propertyRecordcounter+=1

            if line.find("</tr><tr>")!=-1: #we've reached the end of a record, format output and reset counter
                propertyRecordcounter=0 #reset counter when outside a record                                                  
                CaseNumber=parseddata[1]
                Plaintiff=parseddata[2]
                Defendant=parseddata[3]
#                if parseddata[4]=='&nbsp;':
#                    print(CaseNumber)
                Address=parseddata[4]+" "+translatetownship(parseddata[8])+" Ohio"
                Attorney=parseddata[5]
                Appraisal=prepprice(parseddata[7])
                if Appraisal=='&nbsp;':
                    Appraisal=-1
                SaleAmt=prepprice(parseddata[10])
                SaleDate=convertDateFormatMDYSlashdelimited(parseddata[9])
                if 1==1 and parseddata[4]!='&nbsp;':
#CaseNumber,Plaintiff,Name(defendant),Address,Attorney,AttyPhone,Appraisal,Township,SaleDate,SaleAmt
                    #print(CaseNumber,Plaintiff,Defendant,Address,Attorney,appraisal,minbidamt,SaleDate)
                    key=QueryDatabaseIfRecordExists(SaleDate,CaseNumber,Address, Plaintiff,Defendant,Attorney,SoldTo,PID,Zipcode,Appraisal,MinBidAmt,SaleAmt,SaleStatus) 

                    if key==-1: # no results found, enter into database
 #                       print("-Enter"),
                       InsertSaleInfoIntoDB(SaleDate,CaseNumber,Address, Plaintiff,Defendant,Attorney,SoldTo,PID,Zipcode,Appraisal,MinBidAmt,SaleAmt,SaleStatus)
                    elif key==-2:
                        print("uhoh multiple results returned")
                    elif key==-3:
                        print(",unchanged"), #record is unchanged, don't do anything
                    else:
                        print("+"), #record has changed and we are updating it using the key
                        #we DONT want to update Franklin county records as that destroys what the appraisal amount was. As when a property is past its sale date then the appraisal value is replaced with $0.00

            if line.find("</table>")!=-1: #this signals the end of the property list                                                              
                enddataflag=1
        else:
            linecounter+=1
    output=open(outputfilename,"w")
    output.write(data)
    output.close()

#remove table tags and split fields
def ParseTableData1(line):
    removedtdend=stripampersand(line) 
    separated=removedtdend.split("</td><td>")
    #    print(separated)#[11],separated[10])
    if (separated[9]).find("checked")!=-1:
        separated[9]=1
    else:
        separated[9]=0
    
    #print separated
    return separated

#attempt to parse html
#http://segfault.in/2010/07/parsing-html-table-in-python-with-beautifulsoup/ http://stackoverflow.com/questions/6325216/parse-html-table-to-python-list    
def ParseTableData(inputfilename,line):
    from xml.etree import ElementTree as ET
    s = """<table>
  <tr><th>Event</th><th>Start Date</th><th>End Date</th></tr>
  <tr><td>a</td><td>b</td><td>c</td></tr>
  <tr><td>d</td><td>e</td><td>f</td></tr>
  <tr><td>g</td><td>h</td><td>i</td></tr>
</table>
"""
    ss=open(inputfilename,'r')
    s=ss.read()
    table = ET.XML(s)
    rows = iter(table)
    headers = [col.text for col in next(rows)]
    for row in rows:
        values = [col.text for col in row]
        print dict(zip(headers, values))


import datetime
def convertDateFormat(date):
    day=int(date[3:5])
    month=int(date[0:2])
    year=int(date[6:10])
    dt=datetime.date(year,month,day)
    return dt.strftime("%Y-%m-%d")

def convertDateFormatDMYSlashdelimited(date):
    #print(date)
    datesplit=date.split("/")
    #print(datesplit)
    day=int(datesplit[1])
    month=int(datesplit[0])
    year=int(datesplit[2])
    dt=datetime.date(year,month,day)
    return dt.strftime("%Y-%m-%d")

def convertDateFormatMDYSlashdelimited(date):
    #print(date)
    datesplit=date.split("/")
    #print(datesplit)
    day=int(datesplit[1])
    month=int(datesplit[0])
    year=int(datesplit[2])
    dt=datetime.date(year,month,day)
    return dt.strftime("%Y-%m-%d")


########### MAIN ############

import sys
import MySQLdb as mdb
import urllib,urllib2,time

#check if argv[1]!=null and assign to 
#if sys.argv[#
if 1==1:
    if len(sys.argv)>1 and  sys.argv[1]!="":
        inputfilename=sys.argv[1]
    else:
        inputfilename="../HamiltonCtyOhio05142012ExecPropertySales.aspx.html"
        inputfilename="../HamiltonCtyOhio05142012SoldProperty.aspx.html"
    if len(sys.argv)>2 and sys.argv[2]!="":
        outputfilename=sys.argv[2]
    else:
        outputfilename="HamiltonCountyOhioOutput.txt"
    print(inputfilename,outputfilename)
    ProcessFile(inputfilename,outputfilename)
    ProcessSalesFile(inputfilename,outputfilename)
    


#ParseTableData(inputfilename,"bob")
