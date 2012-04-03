#!/usr/bin/python 
# -*- coding: utf-8 -*-

#########
# This program takes the output and puts it in the MySQL database.
#########

import datetime
def convertDateFormat(date):
#    print(date,date[3:5],date[0:2],date[6:10]) #start and stop indices, not start, length indices
    day=int(date[3:5])
    month=int(date[0:2])
    year=int(date[6:10])
    dt=datetime.date(year,month,day) 
    return dt.strftime("%Y-%m-%d")


import csv 
def readCSVInsertIntoDB():
#    data=csv.reader(open('output.txt'))
    data=csv.reader(open('output_geocoded.txt'))
    con = mdb.connect('localhost', 'nicolae', 'ceausescu', 'SheriffSales')
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
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
#                    print(row[4][3:],row[4])
                    if len(row[4])>7:
                        zipcode=int(row[4][3:])
                    else:
                        zipcode=0
                else:
              #      print(row[4])
                    zipcode=int(row[4])
            print(row)

#            cur.execute("INSERT INTO Property(SaleDate,CaseNumber,Address,ZipCode,Appraisal,MinBid,SaleStatus) VALUES ( %s, %s,%s,%i,%f,%f,%s)", (row[0], row[1],row[2],int(row[4]),float(row[5]),float(row[6]),row[7]))
#            cur.execute("INSERT INTO Property(SaleDate,CaseNumber,Address,Appraisal,MinBid,SaleStatus) VALUES ( %s, %s,%s,'%f','%f',%s)", (row[0], row[1],row[2],float(row[5]),float(row[6]),row[7]))
            date=convertDateFormat(row[0])
#            cur.execute("INSERT INTO Property(SaleDate,CaseNumber,Address,SaleStatus) VALUES ( %s, %s,%s,%s)", (row[0], row[1],row[2],row[7]))
            cur.execute("INSERT INTO Property(SaleDate,CaseNumber,Address,SaleStatus,MinBid,Appraisal,ZipCode,Latitude,Longitude) VALUES ( %s, %s,%s,%s,%s,%s,%s,%s,%s)", (date, row[1],row[2],row[7],minbid,appraisal,zipcode,row[8],row[9])) #even though their database types are int/float etc they are entered as strings here....

    con.commit()
    cur.close()
    con.close()  #leave this open so we don't close other connections/?? if we open a connection we should not open another before closing the current one.


def CreateDatabase():
    con = mdb.connect('localhost', 'nicolae', 'ceausescu', 'SheriffSales')
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute("DROP TABLE IF EXISTS Property")
        cur.execute("CREATE TABLE IF NOT EXISTS Property ( id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, SaleDate DATE,CaseNumber VARCHAR(13) NOT NULL, Address VARCHAR(80) NOT NULL, ZipCode INT NOT NULL,Appraisal DECIMAL(12,2) NOT NULL, MinBid DECIMAL (12,2) NOT NULL, SaleStatus VARCHAR(10) NOT NULL, Latitude FLOAT(10,6) NOT NULL, Longitude FLOAT(10,6) NOT NULL)")
    con.commit()
    cur.close()
    con.close()

def QueryDatabase():
    con = mdb.connect('localhost', 'nicolae', 'ceausescu', 'SheriffSales')
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
#    cur.execute("SELECT * FROM IBD100")
        cur.execute("SELECT * FROM Property")
        rows = cur.fetchall()
        for row in rows:                                        
#        print "%s %s" % (row["Symbol"], row["ClosingPrice"])
#        print "%s %s %s" % (row["CaseNumber"], row["MinBid"])
            print "%s-=-%s-=-%s-=-%s" % (row["CaseNumber"], row["SaleDate"], row["Address"], row["MinBid"]) #acts as decimal type
            print "%s-=-%s-=-%s-=-%f" % (row["CaseNumber"], row["SaleDate"], row["Address"], row["MinBid"]) #acts as float
    cur.close()
    con.close()

import MySQLdb as mdb
import sys
#con = mdb.connect('localhost', 'nicolae', 'ceausescu', 'StockMarketData')
CreateDatabase()
readCSVInsertIntoDB()
QueryDatabase()



#https://developers.google.com/maps/articles/phpsqlgeocode
#http://zetcode.com/databases/mysqlpythontutorial/
#http://dev.mysql.com/doc/refman/5.0/en/datetime.html The DATE type is used for values with a date part but no time part. MySQL retrieves and displays DATE values in 'YYYY-MM-DD' format. The supported range is '1000-01-01' to '9999-12-31'. 
#http://docs.python.org/library/csv.html
"""
>>> import datetime
>>> dt = datetime.date(2009, 01, 13)
>>> dt
datetime.date(2009, 1, 13)
>>> dt.isoformat()
'2009-01-13'
>>> dt.strftime("%d/%m/%Y")
'13/01/2009'
"""


#create database SheriffSales; <- did this while logged into the local mysqld on nicolae
# grant all on SheriffSales.* to 'nicolae'@'localhost'; <- perform as root
