#this program takes as input a saved search from the Montgomery County Sheriff sales site
#the input should be the detailed view listing of properties

import re
def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)
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
    pd = re.compile(r'\.\.') #take care of their double periods in numbers
    pa = re.compile(r'\$')
    temp2=temp.strip() #remove whitespace
    p = re.compile(r',') #remove comma in price since that'll screw things up as far as outputting to csv.

    return p.sub('',pa.sub('',pd.sub(',',temp2)))

def UpdateRecordInDatabase(SaleDate,CaseNumber,Address, Plaintiff,Defendant,Attorney,SoldTo,PID,Zipcode,Appraisal,MinBidAmt,SaleAmt,SaleStatus,key):
    con = mdb.connect('localhost', 'nicolae', 'ceausescu', 'SheriffSales')
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        print("UPDATE Property SET SoldTo=%s, SaleAmt=%s, SaleStatus=%s WHERE id=%s" % (SoldTo,SaleAmt,SaleStatus,key)) 
        cur.execute("UPDATE Property SET SoldTo=%s, SaleAmt=%s, SaleStatus=%s WHERE id=%s", (SoldTo,SaleAmt,SaleStatus,key)) 
    con.commit()
    cur.close()
    con.close()

def InsertIntoDB(date,CaseNumber,Address, Plaintiff,Defendant,Attorney,SoldTo,PID,Zipcode,Appraisal,MinBidAmt,SaleAmt,SaleStatus):
    con = mdb.connect('localhost', 'nicolae', 'ceausescu', 'SheriffSales')
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
# check to see if record exists before inserting, if exists check for salestatus change, update saleamt 
        cur.execute("INSERT INTO Property(SaleDate,CaseNumber,Address,SaleStatus,MinBid,Appraisal,ZipCode,Plaintiff,Defendant,Attorney,SoldTo,PID,SaleAmt) VALUES ( %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (date, CaseNumber,Address,SaleStatus,MinBidAmt,Appraisal,Zipcode,Plaintiff,Defendant,Attorney,SoldTo,PID,SaleAmt)) #even though their database types are int/float etc they are entered as strings here.... 
    con.commit()
    cur.close()
    con.close()  

def InsertUpdateIfExistsIntoDB(date,CaseNumber,Address, Plaintiff,Defendant,Attorney,SoldTo,PID,Zipcode,Appraisal,MinBidAmt,SaleAmt,SaleStatus):
    con = mdb.connect('localhost', 'nicolae', 'ceausescu', 'SheriffSales')
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute("INSERT INTO Property(SaleDate,CaseNumber,Address,SaleStatus,MinBid,Appraisal,ZipCode,Plaintiff,Defendant,Attorney,SoldTo,PID,SaleAmt) VALUES ( %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE SoldTo=%s,SaleAmt=%s,SaleStatus=%s", (date, CaseNumber,Address,SaleStatus,MinBidAmt,Appraisal,Zipcode,Plaintiff,Defendant,Attorney,SoldTo,PID,SaleAmt,SoldTo,SaleAmt,SaleStatus)) #even though their database types are int/float etc they are entered as strings here 
    con.commit()
    cur.close()
    con.close()  


def QueryDatabaseIfRecordExists(date,CaseNumber,Address, Plaintiff,Defendant,Attorney,SoldTo,PID,Zipcode,Appraisal,MinBidAmt,SaleAmt,SaleStatus):
    key=-1 #primary keys aren't negative as far as I know. This is the sentinel value
    con = mdb.connect('localhost', 'nicolae', 'ceausescu', 'SheriffSales')
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
# check to see if record exists before inserting, if exists check for salestatus change, update saleamt 
        resultcount=int(cur.execute("SELECT * FROM Property WHERE SaleDate=%s and CaseNumber=%s and Address=%s and MinBid=%s and Appraisal=%s and ZipCode=%s and Plaintiff=%s and Defendant=%s and Attorney=%s and PID=%s ", (date, CaseNumber,Address,MinBidAmt,Appraisal,Zipcode,Plaintiff,Defendant,Attorney,PID)))  # look for match on all fields except those that would've been update after teh property was sold
        #print("SELECT * FROM Property WHERE SaleDate=%s and CaseNumber=%s and Address=%s and MinBid=%s and Appraisal=%s and ZipCode=%s and Plaintiff=%s and Defendant=%s and Attorney=%s and PID=%s and SaleStatus!=%s " % (date, CaseNumber,Address,MinBidAmt,Appraisal,Zipcode,Plaintiff,Defendant,Attorney,PID,SaleStatus))  # look for match on all fields except those that would've been update after teh property was sold
#        resultcount=cur.row_count() can also be used at any time to obtain number of rows returned by the query

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
            if 1==0:
                if date=="2012-04-06":
                    print("--%s--++%s++" %(row['SaleStatus'],SaleStatus))
        elif resultcount>1:
            print("multiple results:%i",resultcount)
            key=-2
            #rows=cur.fetchall()
        else:
            print("no results found"),
            print("SELECT * FROM Property WHERE SaleDate=%s and CaseNumber=%s and Address=%s and MinBid=%s and Appraisal=%s and ZipCode=%s and Plaintiff=%s and Defendant=%s and Attorney=%s and PID=%s " % (date, CaseNumber,Address,MinBidAmt,Appraisal,Zipcode,Plaintiff,Defendant,Attorney,PID))  
#            print("SELECT * FROM Property WHERE SaleDate=%s and CaseNumber=%s and Address=%s and MinBid=%s and Appraisal=%s and ZipCode=%s and Plaintiff=%s and Defendant=%s and Attorney=%s and PID=%s and SaleStatus!=%s " % (date, CaseNumber,Address,MinBidAmt,Appraisal,Zipcode,Plaintiff,Defendant,Attorney,PID,SaleStatus))  # look for match on all fields except those that would've been update after teh property was sold
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
        if (linecounter > 75) and (enddataflag==0): #first valid record starts after line 75
            line1=line.strip()
            linelower=line.lower()
            if linelower.find("<tr class=\"")!=-1: # align=\"center\" valign=\"top\"")!=-1:
                propertyRecordcounter=0
                
            if propertyRecordcounter==10:
                SaleDate=striphtml(line1.rstrip())
#could be done in a switch statement but python doesn't implement them and for simplicity sake I'm not going the dictionary lookup route.
            if propertyRecordcounter==4:
                CaseNumber=striphtml(line1.rstrip())
                print(CaseNumber)
            if propertyRecordcounter==8:
                Address=striphtml(stripampersand(stripcomma(line1.rstrip())))
            if propertyRecordcounter==2:
                Plaintiff=striphtml(stripampersand(stripcomma(line1.rstrip())))
            if propertyRecordcounter==3:
                Defendant=striphtml(stripampersand(stripcomma(line1.rstrip())))
            if propertyRecordcounter==999999916:
                Attorney=striphtml(stripampersand(stripcomma(line1.rstrip())))
            if propertyRecordcounter==99999918:
                SoldTo=striphtml(stripampersand(stripcomma(line1.rstrip())))
            if propertyRecordcounter==7:
                PIDa=striphtml(stripampersand(stripcomma(line1.rstrip())))
                PID=PIDa.strip() #needed an additional strip 
            if propertyRecordcounter==999999927:
                Zipcode=striphtml(line1.rstrip()) #some zips don't exist, are prepended by OH
            if propertyRecordcounter==13:
                SaleStatus=striphtml(stripampersand(stripcomma(line1.rstrip())))
            if propertyRecordcounter==5:
                Appraisal=prepprice(line1)
            if propertyRecordcounter==6:   #I had a record where the minbid or appraisal had two decimal points in it. I suppose that means that they don't typecheck the records and are input as strings and not as numeric types. Need to type check to prevent it occurring in the future
                MinBidAmt=prepprice(line1)
            if propertyRecordcounter==999999941:
                SaleAmt=prepprice(line1) 
            
            propertyRecordcounter+=1
#we've reached the end of a record, output and reset counter
            if line.find("</tr>")!=-1: 
                propertyRecordcounter=0 
#reset counter when outside a record                                                  
                #print(SaleDate,CaseNumber,Address,Plaintiff,Defendant,Attorney,SoldTo,Zipcode,Appraisal,MinBidAmt,SaleStatus)
### Clean up the formatting
                date=SaleDate
                appraisal=Appraisal
                zipcode=Zipcode
                minbid=MinBidAmt
                salestatus=SaleStatus
                saleamt=SaleAmt
                if Appraisal=="" or Appraisal=="in Bid:&nbsp;&nbsp;":
                    appraisal=0.0
                else:
                    appraisal=float(Appraisal)
                    
                if SaleStatus=="NO BID  NO SALE":
                    salestatus="NOBIDNOSALE"
                else:
                    salestatus=SaleStatus

                if MinBidAmt=="":
                    minbid=0.0
                elif MinBidAmt=="SEE ENTRY":
                    minbid=0.0
                elif MinBidAmt=="SEE ENTRY FOR AMOUNTS":
                    minbid=0.0
                else:
                    minbid=float(MinBidAmt)

                if SaleAmt=="":
                    saleamt=-0.01
                else:
                    saleamt=float(SaleAmt)

                if Zipcode=="":
                    zipcode=0
                else:
                    if Zipcode[0:2]=="OH":
                        if len(Zipcode)>7:
                            zipcode=int(Zipcode[3:])
                        else:
                            zipcode=0
                    else:
                        zipcode=int(Zipcode)

                date=convertDateFormatMDYSlashDelimited(SaleDate)
                
###                                
                data+=SaleDate+","+CaseNumber+","+Address+","+ Plaintiff+','+Defendant+','+ PID+',' +Zipcode+","+Appraisal+","+MinBidAmt+","+SaleAmt+','+SaleStatus+"\n"

                if 1==0:
                    key=QueryDatabaseIfRecordExists(date,CaseNumber,Address, Plaintiff,Defendant,Attorney,SoldTo,PID,zipcode,appraisal,minbid,saleamt,salestatus)
                    if key==-1: # no results found, enter into database
                        print("-"),
                        #InsertUpdateIfExistsIntoDB(date,CaseNumber,Address, Plaintiff,Defendant,Attorney,SoldTo,PID,zipcode,appraisal,minbid,saleamt,salestatus)
                        InsertIntoDB(date,CaseNumber,Address, Plaintiff,Defendant,Attorney,SoldTo,PID,zipcode,appraisal,minbid,saleamt,salestatus)
                    elif key==-2:
                        print("uhoh multiple results returned")
                    elif key==-3:
                        print(","), #record is unchanged, don't do anything
                    else:
                        print("+"), #record has changed and we are updating it using the key
                        UpdateRecordInDatabase(date,CaseNumber,Address, Plaintiff,Defendant,Attorney,SoldTo,PID,zipcode,appraisal,minbid,saleamt,salestatus,key)

                else:
                    nine=9
                    #InsertUpdateIfExistsIntoDB(date,CaseNumber,Address, Plaintiff,Defendant,Attorney,SoldTo,PID,zipcode,appraisal,minbid,saleamt,salestatus)


            if line.find("</table>")!=-1: #this signals the end of the property list                                                              
                enddataflag=1
        else:
            linecounter+=1

    output=open(outputfilename,"w")
    output.write(data)
    output.close()


import datetime
def convertDateFormat(date):
    print("I need to strip based on the / delimiter")
    day=int(date[3:5])
    month=int(date[0:2])
    year=int(date[6:10])
    dt=datetime.date(year,month,day)
    return dt.strftime("%Y-%m-%d")
def convertDateFormatMDYSlashDelimited(date):
    datesplit=date.split("/")
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
        inputfilename="WarrenCountyOhio.slsgrid.asp.html"
    if len(sys.argv)>2 and sys.argv[2]!="":
        outputfilename=sys.argv[2]
    else:
        outputfilename="WarrenCountyoutput.txt"
    print(inputfilename,outputfilename)
    ProcessFile(inputfilename,outputfilename)


