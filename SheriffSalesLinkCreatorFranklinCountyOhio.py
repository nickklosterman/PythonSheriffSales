#this program takes as input a saved search from the Franklin County Sheriff sales site
#the input should be the detailed view listing of properties

import re
def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)
def striphtmlAddressFranklinCounty(data):
    #p = re.compile(r'<br />')
    p = re.compile(r'<.*?>')
    return p.sub(' ', data)
def stripspaces(data):
    p = re.compile(r' ')
    return p.sub('+',data)
def stripampersand(data):
    p = re.compile(r'&')
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


def InsertIntoDB(date,CaseNumber,Address, Plaintiff,Defendant,Attorney,SoldTo,PID,Zipcode,Appraisal,MinBidAmt,SaleAmt,SaleStatus):
    con = mdb.connect('localhost', 'nicolae', 'ceausescu', 'SheriffSales')
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
# check to see if record exists before inserting, if exists check for salestatus change, update saleamt 

        if Appraisal>0:
            SaleStatus="ACTIVE"
        else:
            SaleStatus="UNKNOWN" #set to unknown since not sure if cancelled or sold.
            

        cur.execute("INSERT INTO Property(SaleDate,CaseNumber,Address,Appraisal,PID) VALUES ( %s,%s,%s,%s,%s)", (date, CaseNumber,Address,Appraisal,PID)) #even though their database types are int/float etc they are entered as strings here.... 

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
            soldto=row['SoldTo']
            salestatus=row['SaleStatus']
            saleamt=float(row['SaleAmt']) #otherwise is a decimal object coming from MySQL
            if  salestatus!=SaleStatus: # and soldto!=SoldTo:
                #print(saleamt,SaleAmt,salestatus,SaleStatus,soldto,SoldTo)
                print("*"),
            else:
                key=-3 #if salestatus hasn't changed then don't update
#            print(saleamt,SaleAmt,salestatus,SaleStatus,soldto,SoldTo)
#            print(key)
        elif resultcount>1:
            print("multiple results:%i",resultcount)
            key=-2
            #rows=cur.fetchall()
        else:
            print("no results found"),
            print("SELECT * FROM Property WHERE SaleDate=%s and CaseNumber=%s and Address=%s and Appraisal=%s and PID=%s " % (date, CaseNumber,Address,Appraisal,PID))  
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

    for line in AuctionListFile:
        if (linecounter > 150) and (enddataflag==0): #first valid record starts on line 150 in the detailed view
            line1=line.strip()
            linelower=line.lower()
            if linelower.find("<div class=\"parcel\">")!=-1: 
                propertyRecordcounter=0
                PIDflag=0
                #address,pid,case,appr,dep,saledate

#could be done in a switch statement but python doesn't implement them and for simplicity sake I'm not going the dictionary lookup route.

            if propertyRecordcounter==1:
                Address=striphtmlAddressFranklinCounty(stripampersand(stripcomma(line1.rstrip()))).strip()
            if propertyRecordcounter==5 and line.find("<a href=\"http://www.franklincountyoh.metacama.com/do/searchByParcelId?taxDistrict=")!=-1:
                PIDflag=0
                propertyRecordcounter-=2 #back up two spaces
                PID+=striphtml(line1.rstrip())+" " #http://www.franklincountyoh.metacama.com/do/searchByParcelId?taxDistrict=YYY&parcelNbr=XXXXXX&submit=Submit <-- parcel id contains taxdistrict 1st 3 digits and parcelnbr last 6 digits
            if PIDflag==0:    ########<-- I need a better way to handle this as there may be multiple lines of parcel ids for a given record. I've seen up to 5 pids for a single property, how do I enter into the database multiple pids? concatenate  all with a , and deal with in output or just take first PID since one is proly good enough. Or add flag stating addl PIDs?
                if propertyRecordcounter==6:
                    r=striphtml(line1.rstrip())
                    CaseNumber=r[12:].strip()
                if propertyRecordcounter==7:
                    r=striphtml(line1.rstrip())
                    Appraisal=prepprice(r[16:])
                if propertyRecordcounter==8:
                    MinBidAmt=prepprice(line1)  #this is just 10% of appraisal. not minbid
                if propertyRecordcounter==9:
                    t=striphtml(line1) #all ready in MySQL date format
                    SaleDate=t[10:].strip() 
            else:  #handle case when PID specified
                if propertyRecordcounter==8:
                    r=striphtml(line1.rstrip())
                    CaseNumber=r[12:].strip()
                if propertyRecordcounter==9:
                    r=striphtml(line1.rstrip())
                    Appraisal=prepprice(r[16:])
                if propertyRecordcounter==10:
                    MinBidAmt=striphtml(line1.rstrip())
                if propertyRecordcounter==11:
                    t=striphtml(line1) #all ready in MySQL date format
                    SaleDate=t[10:].strip() 


            propertyRecordcounter+=1
            
            

#this next line is semi-redundant, we reset these elsewhere as well.
            if line.find("</div>")!=-1: #we've reached the end of a record, format output and reset counter
                propertyRecordcounter=0 #reset counter when outside a record                                                  
                PIDflag=0
                #data+=SaleDate+","+CaseNumber+","+Address+","+ PID.strip()+',' +Appraisal+"\n"
                PID=""
                if 1==1:
                    date=SaleDate
                    appraisal=Appraisal
                    zipcode=Zipcode
                    minbid=MinBidAmt
                    salestatus=SaleStatus
                    saleamt=SaleAmt
                    key=QueryDatabaseIfRecordExists(date,CaseNumber,Address, Plaintiff,Defendant,Attorney,SoldTo,PID,zipcode,appraisal,minbid,saleamt,salestatus)
                    if key==-1: # no results found, enter into database
                        print("-"),
                        #InsertIntoDB(SaleDate,CaseNumber,Address, Plaintiff,Defendant,Attorney,SoldTo,PID,Zipcode,Appraisal,MinBidAmt,SaleAmt,SaleStatus)
                    elif key==-2:
                        print("uhoh multiple results returned")
                    elif key==-3:
                        print(","), #record is unchanged, don't do anything
                    else:
                        print("+"), #record has changed and we are updating it using the key
                        #we DONT want to update Franklin county records as that destroys what the appraisal amount was. As when a property is past its sale date then the appraisal value is replaced with $0.00

            if line.find(" <!-- InstanceEndEditable -->")!=-1: #this signals the end of the property list                                                              
                enddataflag=1
        else:
            linecounter+=1
    output=open(outputfilename,"w")
    output.write(data)
    output.close()


import datetime
def convertDateFormat(date):
    day=int(date[3:5])
    month=int(date[0:2])
    year=int(date[6:10])
    dt=datetime.date(year,month,day)
    return dt.strftime("%Y-%m-%d")

def convertDateFormatMDYSlashdelimited(date):
    datesplit=date.split("/")
    day=int(datesplit[0])
    month=int(datesplit[1])
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
        inputfilename="FranklinCountyOhio.real-estate.cfm.html"
    if len(sys.argv)>2 and sys.argv[2]!="":
        outputfilename=sys.argv[2]
    else:
        outputfilename="FranklinCountyoutput.txt"
    print(inputfilename,outputfilename)
    ProcessFile(inputfilename,outputfilename)

