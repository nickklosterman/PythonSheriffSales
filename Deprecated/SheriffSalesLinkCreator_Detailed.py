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
    temp2=temp[1:] #remove dollar sign
    temp3=temp2.strip() #remove whitespace
    p = re.compile(r',') #remove comma in price since that'll screw things up as far as outputting to csv.
    return p.sub('',temp3)
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
        #resultcount=int(cur.execute("SELECT * FROM Property WHERE SaleDate=%s and CaseNumber=%s and Address=%s and MinBid=%s and Appraisal=%s and ZipCode=%s and Plaintiff=%s and Defendant=%s and Attorney=%s and PID=%s and SaleStatus!=%s ", (date, CaseNumber,Address,MinBidAmt,Appraisal,Zipcode,Plaintiff,Defendant,Attorney,PID,SaleStatus)))  # look for match on all fields except those that would've been update after teh property was sold
        resultcount=int(cur.execute("SELECT * FROM Property WHERE SaleDate=%s and CaseNumber=%s and Address=%s and MinBid=%s and Appraisal=%s and ZipCode=%s and Plaintiff=%s and Defendant=%s and Attorney=%s and PID=%s ", (date, CaseNumber,Address,MinBidAmt,Appraisal,Zipcode,Plaintiff,Defendant,Attorney,PID)))  # look for match on all fields except those that would've been update after teh property was sold
#        resultcount=int(cur.execute("SELECT * FROM Property WHERE SaleDate=%s and CaseNumber=%s and Address=%s and PID=%s and SaleStatus!=%s and SoldTo!=%s and SaleAmt!=%s", (date, CaseNumber,Address,PID,SaleStatus,SoldTo,SaleAmt)))  
#        resultcount=int(cur.execute("SELECT * FROM Property WHERE SaleDate=%s and CaseNumber=%s and Address=%s and PID=%s and SaleStatus=%s and SoldTo=%s and SaleAmt=%s", (date, CaseNumber,Address,PID,SaleStatus,SoldTo,SaleAmt)))   #if they've been update salestatus,soldto and saleamt will have changed
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
    


def CreateDatabase():
    con = mdb.connect('localhost', 'nicolae', 'ceausescu', 'SheriffSales')
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute("CREATE TABLE IF NOT EXISTS Property ( id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, SaleDate DATE,CaseNumber VARCHAR(13) NOT NULL, Address VARCHAR(80) NOT NULL, ZipCode INT NOT NULL,Plaintiff VARCHAR(45) NOT NULL,Defendant VARCHAR(45) NOT NULL,Attorney VARCHAR(45) NOT NULL, SoldTo VARCHAR(45) NOT NULL , PID VARCHAR(45) NOT NULL,Appraisal DECIMAL(12,2) NOT NULL, MinBid DECIMAL (12,2) NOT NULL, SaleAmt DECIMAL (12,2) , SaleStatus VARCHAR(11) NOT NULL, Latitude FLOAT(10,6) , Longitude FLOAT(10,6) )") #Latitude FLOAT(10,6) NOT NULL, Longitude FLOAT(10,6) NOT NULL)")
    con.commit()
    cur.close()
    con.close()


def DropTableFromDatabase():
    con = mdb.connect('localhost', 'nicolae', 'ceausescu', 'SheriffSales')
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute("DROP TABLE IF EXISTS Property")
    con.commit()
    cur.close()
    con.close()

def QueryDatabase():
    con = mdb.connect('localhost', 'nicolae', 'ceausescu', 'SheriffSales')
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute("SELECT * FROM Property")
        rows = cur.fetchall()
        for row in rows:
#        print "%s %s %s" % (row["CaseNumber"], row["MinBid"])                                                                                                  
            print "%s-=-%s-=-%s-=-%s" % (row["CaseNumber"], row["SaleDate"], row["Address"], row["MinBid"]) #acts as decimal type                                                        
            print "%s-=-%s-=-%s-=-%f" % (row["CaseNumber"], row["SaleDate"], row["Address"], row["MinBid"]) #acts as float                                                               
    cur.close()
    con.close()



def GeocodeDatabase():
    sleep_time = 1.0
    con = mdb.connect('localhost', 'nicolae', 'ceausescu', 'SheriffSales')
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        curUpdate = con.cursor(mdb.cursors.DictCursor)
        resultcount=int(cur.execute("SELECT * FROM Property WHERE Latitude is NULL"))
        print("Need to geocode "+str(resultcount)+" addresses.")
        rows = cur.fetchall()
        counter=0
        out_file_failed = 'geocode_failed.txt'
        outf_failed = open(out_file_failed,'w')
        
        for row in rows:
            counter+=1
            print("Geocoding "+str(counter)+" of "+str(resultcount)+" addresses.")
            if 1==1:
                geocode_data=geocode(row["Address"])
                if len(geocode_data)>1:
                    lat=geocode_data['lat']
                    lon=geocode_data['lng']
                    curUpdate.execute("UPDATE Property SET Latitude=%s, Longitude=%s WHERE id=%s", (lat,lon,row["id"]))  #SELECT count(*) FROM Property WHERE Latitude is NULL 
                else:
                    print("Geocoding of '"+row["Address"]+"' failed with error code "+geocode_data['code'])
                    outf_failed.write(row["Address"]+'\n')
                    outf_failed.flush()
                time.sleep(sleep_time)  
        outf_failed.close()
    con.commit()
    cur.close()
    con.close()

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
        if (linecounter > 150) and (enddataflag==0): #first valid record starts on line 150 in the detailed view
            line1=line.strip()
            linelower=line.lower()
            if linelower.find("td height=\"25\"")!=-1: # align=\"center\" valign=\"top\"")!=-1:
                propertyRecordcounter=0
                SaleDate=striphtml(line1.rstrip())

#could be done in a switch statement but python doesn't implement them and for simplicity sake I'm not going the dictionary lookup route.
            if propertyRecordcounter==3:
                CaseNumber=striphtml(line1.rstrip())
            if propertyRecordcounter==7:
                Address=striphtml(stripampersand(stripcomma(line1.rstrip())))
            if propertyRecordcounter==10:
                Plaintiff=striphtml(stripampersand(stripcomma(line1.rstrip())))
            if propertyRecordcounter==13:
                Defendant=striphtml(stripampersand(stripcomma(line1.rstrip())))
            if propertyRecordcounter==16:
                Attorney=striphtml(stripampersand(stripcomma(line1.rstrip())))
            if propertyRecordcounter==18:
                SoldTo=striphtml(stripampersand(stripcomma(line1.rstrip())))
            if propertyRecordcounter==20:
                PIDa=striphtml(stripampersand(stripcomma(line1.rstrip())))
                PID=PIDa.strip() #needed an additional strip 
            if propertyRecordcounter==27:
                Zipcode=striphtml(line1.rstrip()) #some zips don't exist, are prepended by OH
            if propertyRecordcounter==29:
                SaleStatus=striphtml(stripampersand(stripcomma(line1.rstrip())))
            if propertyRecordcounter==35:
                Appraisal=prepprice(line1)
            if propertyRecordcounter==39:
                MinBidAmt=prepprice(line1) 
            if propertyRecordcounter==41:
                SaleAmt=prepprice(line1) 
            propertyRecordcounter+=1

            if propertyRecordcounter>42: #we've reached the end of a record, output and reset counter
                propertyRecordcounter=0 #reset counter when outside a record                                                  
                #print(SaleDate,CaseNumber,Address,Plaintiff,Defendant,Attorney,SoldTo,Zipcode,Appraisal,MinBidAmt,SaleStatus)
### Clean up the formatting
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

                date=convertDateFormat(SaleDate)
                
###                                
                data+=SaleDate+","+CaseNumber+","+Address+","+ Plaintiff+','+Defendant+','+Attorney+','+SoldTo+','+PID+',' +Zipcode+","+Appraisal+","+MinBidAmt+","+SaleAmt+','+SaleStatus+"\n"

                if 1==1:
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
                    InsertUpdateIfExistsIntoDB(date,CaseNumber,Address, Plaintiff,Defendant,Attorney,SoldTo,PID,zipcode,appraisal,minbid,saleamt,salestatus)


            if line.find("</table>")!=-1: #this signals the end of the property list                                                              
                enddataflag=1
        else:
            linecounter+=1

#create object
     # geocode(Address)
#see if address has been geocoded (i.e. query database)
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





root_url = "http://maps.google.com/maps/geo?"
return_codes = {'200':'SUCCESS',
                '400':'BAD REQUEST',
                '500':'SERVER ERROR',
                '601':'MISSING QUERY',
                '602':'UNKOWN ADDRESS',
                '603':'UNAVAILABLE ADDRESS',
                '604':'UNKOWN DIRECTIONS',
                '610':'BAD KEY',
                '620':'TOO MANY QUERIES'
    }

def geocode(addr,out_fmt='csv'):
    #encode our dictionary of url parameters
    values = {'q' : addr, 'output':out_fmt}
    data = urllib.urlencode(values)
    #set up our request
    url = root_url+data
    req = urllib2.Request(url)
    #make request and read response
    response = urllib2.urlopen(req)
    geodat = response.read().split(',')
    response.close()
    #handle the data returned from google
    code = return_codes[geodat[0]]
    if code == 'SUCCESS':
        code,precision,lat,lng = geodat
        return {'code':code,'precision':precision,'lat':lat,'lng':lng}
    else:
        return {'code':code}



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
        inputfilename="SFLISTAUCTIONDO.CFM.htm"
    if len(sys.argv)>2 and sys.argv[2]!="":
        outputfilename=sys.argv[2]
    else:
        outputfilename="output.txt"
    print(inputfilename,outputfilename)
    CreateDatabase()
    ProcessFile(inputfilename,outputfilename)

GeocodeDatabase()




 #stupid error: you get below when the indentation isn't pure tabs. it must count tabs to determine depthof a call.           
#TabError: inconsistent use of tabs and spaces in indentation    


"""  Need to get debug the &nbsp <-- oiutput produced from summary view
03/02/2012,2011 CV 03915,523 NORTH TIONDA DRIVE  VANDALIA,45377,,,&nbsp;&nbsp;
03/09/2012,2009 CV 06467,20 N. PLUM STREET  PHILLIPSBURG,45354,,,&nbsp;&nbsp;
03/09/2012,2010 CV 06153,209 DEAN DRIVE  FARMERSVILLE,45325,,,&nbsp;&nbsp;
03/16/2012,2009 CV 05646,310 SAN BERNARDINO TRAIL  UNION,45322,,,&nbsp;&nbsp;
03/23/2012,2010 CV 07089,1128 SOUTH PAUL LAURENCE DUNBAR STREET  DAYTON,45408,,,&nbsp;&nbsp;

How do I make a 'not equal to' statement in MySQL? 
   There are a number of ways to do this.                                                                 
   Use:                                                                                                   
   WHERE 'something' <> 'something_else'                                                                  
   or:                                                                                                    
   WHERE 'something' != 'something_else'                                                                  
   As they are identical.                                                                                 
   or you can specify a number of values you don't want to be return from your column/field               
   (my_tablein this example) - a more efficient way of doing things if you have a lot of values:          
   WHERE my_table NOT IN ('something', 'something_else'); 

"""

