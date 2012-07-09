#this program takes as input a saved search from the Montgomery County Sheriff sales site
#the input should be the detailed view listing of properties

_URI="localhost"
_Database="SheriffSales"
_Table="RealEstateSales"

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

def getUsernamePassword(file):
    import linecache
    username=linecache.getline(file,1) #username on 1st line
    password=linecache.getline(file,2) #password on 2nd line
    return username.strip(),password.strip()  #remove the CRLF   

def GetConnection(uri,loginfile,database):
    username,password=getUsernamePassword(loginfile)    
    connection=GetMySQLConnection(uri,username,password,database)
    return connection

def GetMySQLConnection(uri,user,password,database):
    connection=mdb.connect(uri,user,password,database)
    return connection

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

def convertSALETYPEToChar(type):
    uppertype=type.upper()
#month_dict = {"Jan":1,"Feb":2,"Mar":3,"Apr":4, "May":5, "Jun":6,       "Jul":7,"Aug":8,"Sep":9,"Oct":10,"Nov":11,"Dec":12} #http://mail.python.org/pipermail/python-list/2010-January/1231526.html
    type_dict = {     "LAND AND BUILDING":1,  "LAND ONLY":2, "BUILDING ONLY":3}
    return type_dict[uppertype]

def convertSALEVALIDITYToChar(validity):
    uppervalidity=validity.upper()
    validity_dict = {     "VALID SALE":1,    "NOT VALIDATED":2,    "RELATED INDIVIDUALS OR CORPORATIONS":3,     "LIQUIDATION/FORECLOSURE":4,       "NOT OPEN MARKET":5,       "PARTIAL  INTEREST":6,       "LAND CONTRACT OR UNUSUAL FINANCING":7,"EXCESS PERSONAL PP/NOT ARMS LENGTH":8,       "OWNER DISHONESTY IN DESCRIPTION":9,     "SALE INVOLVING MULTIPLE PARCELS":10, "INVALID DATE ON SALE":11, "OUTLIER":12,"PROPERTY CHANGED AFTER SALE":13,"RESALE W/IN 3 YRS":14,
"SALE INCL UNLISTED NEW CONST":15}
    return validity_dict[uppervalidity]

def UpdateRecordInDatabase(row,loginfile):
    con =GetConnection(_URI,loginfile,_Database)
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        print("UPDATE RealEstateSales SET SoldTo=%s, SaleAmt=%s, SaleStatus=%s WHERE id=%s" % (SoldTo,SaleAmt,SaleStatus,key)) 
        cur.execute("UPDATE RealEstateSales SET SoldTo=%s, SaleAmt=%s, SaleStatus=%s WHERE id=%s", (SoldTo,SaleAmt,SaleStatus,key)) 
    con.commit()
    cur.close()
    con.close()

#PARID , CONVNUM , SALEDT , PRICE , OLDOWN , OWNERNAME1 , PARCELLOCATION , MAILINGNAME1 , MAILINGNAME2 , PADDR1 , PADDR2 , PADDR3 , CLASS , ACRES , TAXABLELAND , TAXABLEBLDG , TAXABLETOTAL , ASMTLAND , ASMTBLDG , ASMTTOTAL , SALETYPE , SALEVALIDITY , DYTNCRDT ,Latitude FLOAT(10,6) , Longitude FLOAT(10,6) )") 
#def InsertIntoDB(date,row): #PARID,PARCELLOCATION,SALETYPE,SALEVALIDITY):
def InsertIntoDB(row,loginfile): #PARID,PARCELLOCATION,SALETYPE,SALEVALIDITY):
    con =GetConnection(_URI,loginfile,_Database)
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        date=convertDateFormat(row["SALEDTE"])
        saletype=convertSALETYPEToChar(row['SALETYPE'])
        salevalidity=convertSALEVALIDITYToChar(row['SALEVALIDITY'])
        cur.execute("INSERT INTO RealEstateSales(SALEDT,PARID,PARCELLOCATION,SALETYPE,SALEVALIDITY,PRICE) VALUES ( %s,%s,%s,%s,%s,%s)", (date, row['PARID'],row['PARCELLOCATION'],saletype,salevalidity,row['PRICE'])) #even though their database types are int/float etc they are entered as strings here.... 
    con.commit()
    cur.close()
    con.close()  


def InsertUpdateIfExistsIntoDB(row,loginfile): #date,row): #PARID,PARCELLOCATION,SALETYPE,SALEVALIDITY,PRICE):
    con =GetConnection(_URI,loginfile,_Database)
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


def QueryDatabaseIfRecordExists(row,loginfile):
    key=-1 #primary keys aren't negative as far as I know. This is the sentinel value
    con =GetConnection(_URI,loginfile,_Database)
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)        
        date=convertDateFormat(row["SALEDTE"])
        parid=row['PARID']
        parcellocation=row['PARCELLOCATION']
        # check to see if record exists before inserting, if exists check for salestatus change, update saleamt 
        resultcount=int(cur.execute("SELECT id FROM RealEstateSales WHERE SALEDT=%s and PARID LIKE %s and PARCELLOCATION LIKE %s", (date, parid, parcellocation )))  # look for match on all fields except those that would've been update after teh property was sold
        if resultcount==1:
            row=cur.fetchone()
            key=int(row['id'])
            print("+++++++++++++++++++++++++match SALEDT=%s and PARID=%s and PARCELLOCATION=%s " % (date, parid,parcellocation)) 
        elif resultcount>1:
            print("multiple results:%i",resultcount)
            key=-2
        else:
            print("no results found for SALEDT=%s and PARID=%s and PARCELLOCATION=%s " % (date, parid,parcellocation)) 
#            print("SELECT * FROM RealEstateSales WHERE SALEDT=%s and PARID=%s and PARCELLOCATION=%s " % (date, parid,parcellocation))
    cur.close()
    con.close()  
    return int(key) #otherwise it is a long


def CreateDatabase(loginfile):
    con =GetConnection(_URI,loginfile,_Database)
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute("CREATE TABLE IF NOT EXISTS RealEstateSales ( id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, PARID VARCHAR(20), CONVNUM INT, SALEDT DATE, PRICE INT, OLDOWN VARCHAR(33), OWNERNAME1 VARCHAR(33), PARCELLOCATION VARCHAR(45) NOT NULL, MAILINGNAME1 VARCHAR(45), MAILINGNAME2 VARCHAR(45), PADDR1 VARCHAR(45), PADDR2 VARCHAR(45), PADDR3 VARCHAR(45), CLASS CHAR, ACRES FLOAT(8,6), TAXABLELAND INT, TAXABLEBLDG INT, TAXABLETOTAL INT, ASMTLAND INT, ASMTBLDG INT, ASMTTOTAL INT, SALETYPE CHAR, SALEVALIDITY CHAR, DYTNCRDT CHAR,Latitude FLOAT(10,6) , Longitude FLOAT(10,6) )") 
# TIme vs space tradeoff. Not doing mapping/coding of 1->Bob 2->Rob etc will save time (no conversion) but eats up space. However, the same amount of data is transmitted regardless. If you had the client instead of the mysql server do the conversion less data is transmitted but then the processing is done by the client. So hopefully they have a faster comp than the server. This may or may not be the case but it also frees up the server for doing more requests
    con.commit()
    cur.close()
    con.close()


def DropTableFromDatabase(loginfile):
    con =GetConnection(_URI,loginfile,_Database)
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute("DROP TABLE IF EXISTS RealEstateSales")
    con.commit()
    cur.close()
    con.close()

def CSVProcessFile(inputfilename,outputfilename,loginfile):
    print("Using input:%s and output:%s" % (inputfilename,outputfilename))
    #csvreader=csv.reader(open(inputfilename,'rb'),delimiter=',')    
#http://www.doughellmann.com/PyMOTW/csv/index.html 
    csvfile=open(inputfilename,'rb')
    try:
        reader=csv.DictReader(csvfile) #the dictreader method is superior to plain indexing. If the columns move but are still called the same things then our code won't break, whereas addressing by index will
        for row in reader:
            if 1==1:
                key=QueryDatabaseIfRecordExists(row,loginfile)
                if key==-1: # no results found, enter into database
                    print("-"),
                        #InsertUpdateIfExistsIntoDB(date,CaseNumber,Address, Plaintiff,Defendant,Attorney,SoldTo,PID,zipcode,appraisal,minbid,saleamt,salestatus)
                    InsertIntoDB(row,loginfile) 
                elif key==-2:
                    print("uhoh multiple results returned")
                elif key==-3:
                    print(","), #record is unchanged, don't do anything
                else:
                    print("+"), #record present, for real estate sales nothing changes so we don't need to update

#["SALEDTE"] ["PARID"] ["PRICE"] ["ACRES"] ["SALETYPE"] ["SALEVALIDITY"]
    finally: 
        csvfile.close()
    


########### MAIN ############
import csv
import sys
import MySQLdb as mdb
import getopt


inputfilename="RealEstateSalesData/MontgomeryCountyOhio/temp.csv" #SALES_2012_RES.csv"
inputfilename="RealEstateSalesData/MontgomeryCountyOhio/SALES_2012_RES.csv"
outputfilename="RealEstateSalesMontgomeryCtyOhiooutput.txt"
loginfile="/home/nicolae/.mysqllogin"
try:
    options, remainder = getopt.gnu_getopt(sys.argv[1:], 'i:o:l:', ['--input=',
                                                                    '--output=', 
                                                                    '--loginfile=',
                                                                    ])
except getopt.GetoptError, err:
        # print help information and exit:
    print str(err) # will print something like "option -a not recognized"
        #usage()
    sys.exit(2)

for opt, arg in options:
    if opt in ('-o', '--output'):
        outputfilename = arg
    elif opt in ('-i', '--input'):
        inputfilename = arg
    elif opt in ('-l', '--loginfile'):
        loginfile = arg
    elif opt == '--version':
        version = arg

print(inputfilename,outputfilename,loginfile)
#DropTableFromDatabase(loginfile)
CreateDatabase(loginfile)
CSVProcessFile(inputfilename,outputfilename,loginfile)


#http://docs.python.org/library/getopt.html
