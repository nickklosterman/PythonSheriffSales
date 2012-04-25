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
        print("UPDATE RealEstateSales SET SoldTo=%s, SaleAmt=%s, SaleStatus=%s WHERE id=%s" % (SoldTo,SaleAmt,SaleStatus,key)) 
        cur.execute("UPDATE RealEstateSales SET SoldTo=%s, SaleAmt=%s, SaleStatus=%s WHERE id=%s", (SoldTo,SaleAmt,SaleStatus,key)) 
    con.commit()
    cur.close()
    con.close()

def convertSALETYPEToChar(type):
    uppertype=type.upper()
#month_dict = {"Jan":1,"Feb":2,"Mar":3,"Apr":4, "May":5, "Jun":6,       "Jul":7,"Aug":8,"Sep":9,"Oct":10,"Nov":11,"Dec":12} #http://mail.python.org/pipermail/python-list/2010-January/1231526.html
    type_dict = {     "LAND AND BUILDING":1,  "LAND ONLY":2}
    return type_dict[uppertype]

def convertSALEVALIDITYToChar(validity):
    uppervalidity=validity.upper()
    validity_dict = {     "VALID SALE":1,    "NOT VALIDATED":2,    "RELATED INDIVIDUALS OR CORPORATIONS":3,     "LIQUIDATION/FORECLOSURE":4,       "NOT OPEN MARKET":5,       "PARTIAL  INTEREST":6,       "LAND CONTRACT OR UNUSUAL FINANCING":7,"EXCESS PERSONAL PP/NOT ARMS LENGTH":8,       "OWNER DISHONESTY IN DESCRIPTION":9,     "SALE INVOLVING MULTIPLE PARCELS":10, "INVALID DATE ON SALE":11, "OUTLIER":12,"PROPERTY CHANGED AFTER SALE":13,"RESALE W/IN 3 YRS":14,
"SALE INCL UNLISTED NEW CONST":15}
    return validity_dict[uppervalidity]




#PARID , CONVNUM , SALEDT , PRICE , OLDOWN , OWNERNAME1 , PARCELLOCATION , MAILINGNAME1 , MAILINGNAME2 , PADDR1 , PADDR2 , PADDR3 , CLASS , ACRES , TAXABLELAND , TAXABLEBLDG , TAXABLETOTAL , ASMTLAND , ASMTBLDG , ASMTTOTAL , SALETYPE , SALEVALIDITY , DYTNCRDT ,Latitude FLOAT(10,6) , Longitude FLOAT(10,6) )") 
#def InsertIntoDB(date,row): #PARID,PARCELLOCATION,SALETYPE,SALEVALIDITY):
def InsertIntoDB(row): #PARID,PARCELLOCATION,SALETYPE,SALEVALIDITY):
    con = mdb.connect('localhost', 'nicolae', 'ceausescu', 'SheriffSales')
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        date=convertDateFormat(row["SALEDTE"])
        saletype=convertSALETYPEToChar(row['SALETYPE'])
        salevalidity=convertSALEVALIDITYToChar(row['SALEVALIDITY'])
        cur.execute("INSERT INTO RealEstateSales(SALEDT,PARID,PARCELLOCATION,SALETYPE,SALEVALIDITY,PRICE) VALUES ( %s,%s,%s,%s,%s,%s)", (date, row['PARID'],row['PARCELLOCATION'],saletype,salevalidity,row['PRICE'])) #even though their database types are int/float etc they are entered as strings here.... 
    con.commit()
    cur.close()
    con.close()  


def InsertUpdateIfExistsIntoDB(row): #date,row): #PARID,PARCELLOCATION,SALETYPE,SALEVALIDITY,PRICE):
    con = mdb.connect('localhost', 'nicolae', 'ceausescu', 'SheriffSales')
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        date=convertDateFormat(row["SALEDTE"])
        saletype=convertSALETYPEToChar(row['SALETYPE'])
        salevalidity=convertSALEVALIDITYToChar(row['SALEVALIDITY'])
#        cur.execute("INSERT INTO RealEstateSales(SALEDT,PARID,PARCELLOCATION,SALETYPE,SALEVALIDITY) VALUES ( %s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE PRICE=%s", (date, PARID,PARCELLOCATION,saletype,salevalidity,PRICE)) #even though their database types are int/float etc they are entered as strings here.... 
        cur.execute("INSERT INTO RealEstateSales(SALEDT,PARID,PARCELLOCATION,SALETYPE,SALEVALIDITY) VALUES ( %s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE PRICE=%s", (date, row['PARID'],row['PARCELLOCATION'],saletype,salevalidity,row['PRICE'])) #even though their database types are int/float etc they are entered as strings here.... 

    con.commit()
    cur.close()
    con.close()  


def QueryDatabaseIfRecordExists(date,PARID,PARCELLOCATION):
    key=-1 #primary keys aren't negative as far as I know. This is the sentinel value
    con = mdb.connect('localhost', 'nicolae', 'ceausescu', 'SheriffSales')
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
# check to see if record exists before inserting, if exists check for salestatus change, update saleamt 
        resultcount=int(cur.execute("SELECT * FROM RealEstateSales WHERE SALEDT=%s and PARID=%s and PARCELLOCATION=%s ", (date, PARID,PARCELLOCATION)))  # look for match on all fields except those that would've been update after teh property was sold
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
            print("SELECT * FROM RealEstateSales WHERE SaleDate=%s and CaseNumber=%s and Address=%s and MinBid=%s and Appraisal=%s and ZipCode=%s and Plaintiff=%s and Defendant=%s and Attorney=%s and PID=%s " % (date, CaseNumber,Address,MinBidAmt,Appraisal,Zipcode,Plaintiff,Defendant,Attorney,PID))  
#            print("SELECT * FROM RealEstateSales WHERE SaleDate=%s and CaseNumber=%s and Address=%s and MinBid=%s and Appraisal=%s and ZipCode=%s and Plaintiff=%s and Defendant=%s and Attorney=%s and PID=%s and SaleStatus!=%s " % (date, CaseNumber,Address,MinBidAmt,Appraisal,Zipcode,Plaintiff,Defendant,Attorney,PID,SaleStatus))  # look for match on all fields except those that would've been update after teh property was sold
    cur.close()
    con.close()  
    return int(key) #otherwise it is a long


def CreateDatabase():
    con = mdb.connect('localhost', 'nicolae', 'ceausescu', 'SheriffSales')
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute("CREATE TABLE IF NOT EXISTS RealEstateSales ( id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, PARID VARCHAR(20), CONVNUM INT, SALEDT DATE, PRICE INT, OLDOWN VARCHAR(33), OWNERNAME1 VARCHAR(33), PARCELLOCATION VARCHAR(45) NOT NULL, MAILINGNAME1 VARCHAR(45), MAILINGNAME2 VARCHAR(45), PADDR1 VARCHAR(45), PADDR2 VARCHAR(45), PADDR3 VARCHAR(45), CLASS CHAR, ACRES FLOAT(8,6), TAXABLELAND INT, TAXABLEBLDG INT, TAXABLETOTAL INT, ASMTLAND INT, ASMTBLDG INT, ASMTTOTAL INT, SALETYPE CHAR, SALEVALIDITY CHAR, DYTNCRDT CHAR,Latitude FLOAT(10,6) , Longitude FLOAT(10,6) )") 
# TIme vs space tradeoff. Not doing mapping/coding of 1->Bob 2->Rob etc will save time (no conversion) but eats up space. However, the same amount of data is transmitted regardless. If you had the client instead of the mysql server do the conversion less data is transmitted but then the processing is done by the client. So hopefully they have a faster comp than the server. This may or may not be the case but it also frees up the server for doing more requests
    con.commit()
    cur.close()
    con.close()


def DropTableFromDatabase():
    con = mdb.connect('localhost', 'nicolae', 'ceausescu', 'SheriffSales')
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute("DROP TABLE IF EXISTS RealEstateSales")
    con.commit()
    cur.close()
    con.close()

def CSVProcessFile(inputfilename,outputfilename):
    print("Using input:%s and output:%s" % (inputfilename,outputfilename))
    #csvreader=csv.reader(open(inputfilename,'rb'),delimiter=',')    
#http://www.doughellmann.com/PyMOTW/csv/index.html 
    csvfile=open(inputfilename,'rb')
    try:
        reader=csv.DictReader(csvfile) #the dictreader method is superior to plain indexing. If the columns move but are still called the same things then our code won't break, whereas addressing by index will
        for row in reader:#csvreader:
#            print(date)
 #           print(date,row["PARID"],row["PARCELLOCATION"],row["SALETYPE"])#,row["SALEVALIDITY)"]) 
  #          print(row["SALEVALIDITY"])

            InsertIntoDB(row) #["PARID"],row["PARCELLOCATION"],row["SALETYPE"],row["SALEVALIDITY"]) #             InsertIntoDB(date,row) # then just have the funct parse and send what it wants
            #InsertIntoDB(date,row) #["PARID"],row["PARCELLOCATION"],row["SALETYPE"],row["SALEVALIDITY"]) #             InsertIntoDB(date,row) # then just have the funct parse and send what it wants
#            InsertIntoDBUpdateIfExists(date,row["PARID"],row["PARCELLOCATION"],row["SALETYPE"],row["SALEVALIDITY"]) #             InsertIntoDB(date,row) # then just have the funct parse and send what it wants
#           InsertUpdateIfExistsIntoDB(date,row) #             InsertIntoDB(date,row) # then just have the funct parse and send what it wants

#
#["SALEDTE"] ["PARID"] ["PRICE"] ["ACRES"] ["SALETYPE"] ["SALEVALIDITY"]
    finally: 
        csvfile.close()

import datetime
def convertDateFormat(date):
    splitdate=date.split("-")    
    day=int(splitdate[0])
    month=convert3LetterMonthToNumber(splitdate[1])
    year=int(splitdate[2])+2000
    dt=datetime.date(year,month,day)
    return dt.strftime("%Y-%m-%d")

def convert3LetterMonthToNumber(month):
    uppermonth=month.upper()
#month_dict = {"Jan":1,"Feb":2,"Mar":3,"Apr":4, "May":5, "Jun":6,       "Jul":7,"Aug":8,"Sep":9,"Oct":10,"Nov":11,"Dec":12} #http://mail.python.org/pipermail/python-list/2010-January/1231526.html
#http://www.wellho.net/mouth/2951_Lots-of-way-of-converting-3-letter-month-abbreviations-to-numbers.html
#doing conversion in mysql Query:http://p2p.wrox.com/sql-server-2005/70107-converting-month-name-month-number.html
    month_dict = {"JAN":1,"FEB":2,"MAR":3,"APR":4, "MAY":5, "JUN":6,"JUL":7,"AUG":8,"SEP":9,"OCT":10,"NOV":11,"DEC":12}
    return month_dict[uppermonth]
    




########### MAIN ############
import csv
import sys
import MySQLdb as mdb
import urllib,urllib2,time

#check if argv[1]!=null and assign to 
#if sys.argv[#
if 1==1:
    if len(sys.argv)>1 and  sys.argv[1]!="":
        inputfilename=sys.argv[1]
    else:
        inputfilename="RealEstateSalesData/MontgomeryCountyOhio/temp.csv" #SALES_2012_RES.csv"
        inputfilename="RealEstateSalesData/MontgomeryCountyOhio/SALES_2012_RES.csv"
    if len(sys.argv)>2 and sys.argv[2]!="":
        outputfilename=sys.argv[2]
    else:
        outputfilename="RealEstateSalesMontgomeryCtyOhiooutput.txt"
    print(inputfilename,outputfilename)
    DropTableFromDatabase()
    CreateDatabase()
    CSVProcessFile(inputfilename,outputfilename)

