#!/usr/bin/python3
#this program takes as input a saved search from the Montgomery County Sheriff sales site
#the input should be the detailed view listing of properties

_URI="localhost"
_Database="SheriffSales"
_Table="RentalRegistrationMontgomeryCountyOhio2013"

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

def InsertIntoDBOrig(row,cur):
    cur.execute("INSERT INTO %s (TAX_DISTRICT, PARCEL, LOCATION, NUMBER_OF_UNITS ) VALUES ( %s,%s,%s,%s)", (_Table, row['TAX DISTRICT'], row['PARCEL'],row['LOCATION'],row['NUMBER UNITS'])) #even though their database types are int/float etc they are entered as strings here.... 


def InsertIntoDB(row):
    con =GetConnection(_URI,loginfile,_Database)
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
#        cur.execute("INSERT INTO %s (TAX_DISTRICT, PARCEL, LOCATION, NUMBER_OF_UNITS ) VALUES ( %s,%s,%s,%s)" % (_Table, row['TAX DISTRICT'], row['PARCEL'],row['LOCATION'],row['NUMBER UNITS'])) #even though their database types are int/float etc they are entered as strings here.... 
        print("INSERT INTO %s ( PARCEL, LOCATION ) VALUES ( \"%s\",\"%s\")" % (_Table, row['PARCEL'],row['LOCATION']))
        cur.execute("INSERT INTO %s ( PARCEL, LOCATION ) VALUES (\" %s \",\"%s\")" % (_Table, row['PARCEL'],row['LOCATION'])) #even though their database types are int/float etc they are entered as strings here.... 
        con.commit()
        cur.close()
        con.close()  

def CreateDatabase(loginfile):
    con =GetConnection(_URI,loginfile,_Database)
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute("CREATE TABLE IF NOT EXISTS %s ( id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, TAX_DISTRICT VARCHAR(20), PARCEL VARCHAR(18), LOCATION VARCHAR(45) NOT NULL, NUMBER_OF_UNITS INT NOT NULL, Latitude FLOAT(10,6) , Longitude FLOAT(10,6) )"%(_Table)) 
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

def CSVProcessFile(inputfilename,loginfile):
    print("Using input:%s " % (inputfilename))
    csvfile=open(inputfilename,'rt')
    try:
#        reader=csv.DictReader(csvfile) #the dictreader method is superior to plain indexing. If the columns move but are still called the same things then our code won't break, whereas addressing by index will
        reader=csv.DictReader(csvfile) 
        print(reader.fieldnames)
        try:
            for row in reader:
#                print(row)
                InsertIntoDB(row) 
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
    filelist= glob.glob(directory+'rentalreg_*.csv')
    return filelist

########### MAIN ############
import csv
import sys
#import MySQLdb as mdb # no workie for python3 
import pymysql as mdb #  git clone https://github.com/petehunt/PyMySQL.git ; ./build-py3k.sh  ; cd py3k; sudo python setup.py install ; and that should install it
import getopt
import glob # flro globbing csv files in the input directory

inputdirectory="RentalRegistration/MontgomeryCountyOhio/"
loginfile="/home/nicolae/.mysqllogin"

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
print("Dropping and then creating the database.")
DropTableFromDatabase(loginfile)
CreateDatabase(loginfile)

filelist = getFileList(inputdirectory) 
for item in filelist:
    print("processing "+item) 
    CSVProcessFile(item,loginfile)
print("You now need to geocode the database!!!")
print("print out status of the records being processed. get # of lines and show how many have gone through. X of Y processed.")
#http://docs.python.org/library/getopt.html
