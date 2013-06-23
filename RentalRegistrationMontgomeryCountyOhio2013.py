#!/usr/bin/python3
#this program takes as input a saved search from the Montgomery County Sheriff sales site
#the input should be the detailed view listing of properties

_URI="localhost"
_Database="SheriffSales"
_Table="RentalRegistrationMontgomeryCountyOhio2013"
_INSERT=0
_UPDATE=1

def getUsernamePassword(file):
    import linecache
    username=linecache.getline(file,1) #username on 1st line
    password=linecache.getline(file,2) #password on 2nd line
    return username.strip(),password.strip()  #remove the CRLF   

def getMySQLDetails(file):
    import linecache
    username=linecache.getline(file,1) #username on 1st line
    password=linecache.getline(file,2) #password on 2nd line
    host=linecache.getline(file,3) 
    port=linecache.getline(file,4) 
    database=linecache.getline(file,5) 
    table=linecache.getline(file,6) 

    return username.strip(),password.strip(),host.strip(),int(port.strip()),database.strip(),table.strip()  #remove the CRLF   


def GetConnection(uri,loginfile,database_): #uri,database_ are discarded
    username,password,host,port,database,table=getMySQLDetails(loginfile)    
    connection=GetMySQLConnection(host,port,username,password,database)
    return connection

def GetMySQLConnection(uri,dbport,username,password,database):
    connection=mdb.connect(host=uri,port=dbport,user=username,passwd=password,db=database)
    return connection

def InsertIntoDB(row):
    con =GetConnection(_URI,loginfile,_Database)
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        #the tax district is encoded in the parcel as the first character set
#        cur.execute("INSERT INTO %s ( PARCEL, LOCATION, NUMBER_OF_UNITS ) VALUES ( '%s','%s',%s)" % (_Table,  row['PARCEL'],row['LOCATION'],int(row['NUMBER UNITS']),)) #even though their database types are int/float etc they are entered as strings here.... 
        cur.execute("INSERT INTO %s ( TAX_DISTRICT, DISTRICT_NAME, PARCEL, LOCATION, NUMBER_OF_UNITS ) VALUES ( '%s','%s','%s','%s',%s)" % (_Table, row['TAX_DISTRICT'], row['DISTRICT_NAME'], row['PARCEL'],row['LOCATION'],int(row['NUMBER UNITS']),)) #even though their database types are int/float etc they are entered as strings here.... 
    con.commit()
    cur.close()
    con.close()  

def InsertIntoDB2(row,cur):  #this guy needs to be tested to see if it speeds things up
    cur.execute("INSERT INTO %s ( TAX_DISTRICT, DISTRICT_NAME, PARCEL, LOCATION, NUMBER_OF_UNITS ) VALUES ( '%s','%s','%s','%s',%s)" % (_Table, row['TAX_DISTRICT'], row['DISTRICT_NAME'], row['PARCEL'],row['LOCATION'],int(row['NUMBER UNITS']),)) #even though their database types are int/float etc they are entered as strings here.... 

def CreateDatabase(loginfile):
    con =GetConnection(_URI,loginfile,_Database)
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute("CREATE TABLE IF NOT EXISTS %s ( id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,TAX_DISTRICT VARCHAR(5), DISTRICT_NAME VARCHAR(45), PARCEL VARCHAR(18), LOCATION VARCHAR(45) NOT NULL, NUMBER_OF_UNITS INT NOT NULL, Latitude FLOAT(10,6) , Longitude FLOAT(10,6) )"%(_Table)) 
    con.commit()
    cur.close()
    con.close()

def DropTableFromDatabase(loginfile):
    con =GetConnection(_URI,loginfile,_Database)
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute("DROP TABLE IF EXISTS %s" % (_Table) )
    con.commit()
    cur.close()
    con.close()


def UpdateRecordInDatabase(con,key,TaxDistrict,DistrictName):
 #   con =GetConnection(_URI,loginfile,_Database)
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        print("U", end="") 
        querystring=("UPDATE %s SET TAX_DISTRICT='%s', DISTRICT_NAME='%s' WHERE id=%s" % (_Table,TaxDistrict,DistrictName,key)) 
#        print(querystring)
        cur.execute("UPDATE %s SET TAX_DISTRICT='%s', DISTRICT_NAME='%s' WHERE id=%s" % (_Table,TaxDistrict,DistrictName,key)) 
    con.commit()
    cur.close()
#    con.close()

# def UpdateRecordInDatabase(cur,key,TaxDistrict,DistrictName):
#    cur.execute("UPDATE %s SET TAX_DISTRICT=%s, DISTRICT_NAME=%s WHERE id=%s" % (_Table,TaxDistrict,DistrictName,key)) 

def QueryDatabaseIfRecordExists(con,Parcel,Location,NumberOfUnits): #I could proly query on lat and long since they are pretty unique themselves.
    key=-1 #primary keys aren't negative as far as I know. This is the sentinel value
#    con = GetConnection(_URI,loginfile,_Database)
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        querystring=("SELECT * FROM %s WHERE PARCEL='%s' and LOCATION='%s' and NUMBER_OF_UNITS=%s and ISNULL(TAX_DISTRICT)" % (_Table,Parcel,Location,NumberOfUnits))  # look for match on all fields except those that would've been update after teh property was sold
        print(querystring)
        resultcount=int(cur.execute("SELECT * FROM %s WHERE PARCEL='%s' and LOCATION='%s' and NUMBER_OF_UNITS=%s and ISNULL(TAX_DISTRICT)" % (_Table,Parcel,Location,NumberOfUnits)))  # look for match on all fields except those that would've been update after teh property was sold
        print("resultcount:"+str(resultcount))
        if resultcount == 1 :
            print("I think you are failing here")
            row=cur.fetchone()
            print("do we get here")
            key=int(row['id'])
        elif resultcount>1:
            print("multiple results:%i",resultcount)
            key=-2
    cur.close()
    print("is the prob here")
#    con.close()  
    return int(key) #without the cast it is of type long


# def QueryDatabaseIfRecordExists(cur,Parcel,Location,NumberOfUnits): #I could proly query on lat and long since they are pretty unique themselves.
#     key=-1 #primary keys aren't negative as far as I know. This is the sentinel value
#     resultcount=int(cur.execute("SELECT * FROM %s WHERE PARCEL=%s and LOCATION=%s and NUMBER_OF_UNITS=%s" % (_Table,Parcel,Location,NumberOfUnits)))  # look for match on all fields except those that would've been update after teh property was sold
#     if resultcount == 1 :
#         row=cur.fetchone()
#         key=int(row['id'])
#     elif resultcount>1:
#         print("multiple results:%i",resultcount)
#         key=-2
#     return int(key) #without the cast it is of type long



def CSVProcessFile(inputfilename,loginfile):
    print("Using input:%s " % (inputfilename))
    csvfile=open(inputfilename,'rt')
    try:
#        reader=csv.DictReader(csvfile) #the dictreader method is superior to plain indexing. If the columns move but are still called the same things then our code won't break, whereas addressing by index will
        reader=csv.DictReader(csvfile) 
#        print(reader.fieldnames)
        con =GetConnection(_URI,loginfile,_Database)
        try:
            for row in reader:
#                print(row)
                if _INSERT == 1:
                    InsertIntoDB(row) 
                if _UPDATE == 1:

                    returnkey=QueryDatabaseIfRecordExists(con,row['PARCEL'],row['LOCATION'],row['NUMBER UNITS']);
                    if returnkey > 0 :
                        if 'TAX DISTRICT' in row:
                            UpdateRecordInDatabase(con,returnkey,row['TAX DISTRICT'],row['DISTRICT NAME'])
                            con.close()
                        elif 'TAX_DISTRICT' in row:
                            print("----------------tax_district----------------")
                            print(returnkey,row['TAX_DISTRICT'],row['DISTRICT NAME'])
                            UpdateRecordInDatabase(con,returnkey,row['TAX_DISTRICT'],row['DISTRICT NAME'])
#                            con.close()
                        else :
                            print("uh oh not updating")
        except csv.Error as e:
            sys.exit(e)

    except csv.Error as e:
        print("something went wrong in CSVProcessFile for"+inputfilename+" "+e)
    finally: 
            csvfile.close()
    
def CSVProcessFileOrig(inputfilename,loginfile):
    print("Using input:%s " % (inputfilename))
    csvfile=open(inputfilename,'rb')
    con =GetConnection(_URI,loginfile,_Database)
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        try:
            reader=csv.DictReader(csvfile) #the dictreader method is superior to plain indexing. If the columns move but are still called the same things then our code won't break, whereas addressing by index will
            reader.next()  #skip over the first line which holds a header
            for row in reader:
                InsertIntoDB(row,cur) 
        except:
            print("something went wrong in CSVProcessFile for"+inputfilename)
        finally: 
            csvfile.close()
            con.commit()
            cur.close()
            con.close()  
    
def getFileList(directory):
    filelist= sorted(glob.glob(directory+'rentalreg_*.csv'))
    return filelist

########### MAIN ############
import csv
import sys
#import MySQLdb as mdb # no workie for python3 
import pymysql as mdb #  git clone https://github.com/petehunt/PyMySQL.git ; ./build-py3k.sh  ; cd py3k; sudo python setup.py install ; and that should install it
import getopt
import glob # for globbing csv files in the input directory

import os

inputdirectory="RentalRegistration/MontgomeryCountyOhio/"
loginfile=os.path.expanduser("~/.mysqllogin_rentalreg")

try:
    options, remainder = getopt.gnu_getopt(sys.argv[1:], 'i:l:', ['--input=',
                                                                    '--loginfile=',
                                                                    ])
except getopt.GetoptError as err:
        # print help information and exit:
    print(str(err)) # will print something like "option -a not recognized"
        #usage()
    sys.exit(2)

for opt, arg in options:
    if opt in ('-i', '--input'):
        inputfilename = arg
    elif opt in ('-l', '--loginfile'):
        loginfile = arg
    elif opt == '--version':
        version = arg

print(inputdirectory,loginfile)
#with ~25000 records to geocode that takes ~10 days due to google limits
#print("Dropping  the database.")
#DropTableFromDatabase(loginfile)
#print("(re)Creating the database.")
#CreateDatabase(loginfile)

filelist = getFileList(inputdirectory) 
for item in filelist:
    print("processing "+item) 
    CSVProcessFile(item,loginfile)
print("You now need to geocode the database!!!")
print("print out status of the records being processed. get # of lines and show how many have gone through. X of Y processed.")
print("test the insert function that reuses the cursor")
