#!/usr/bin/python2
#this needs to be run with python2 bc the MySQLdb library isn't available in py3

#this program geocodes a database
import geocodeV2

_Table='RentalRegistrationMontgomeryCountyOhio2014'
_Outfile = 'geocode_rentalreg_failed.txt'

def getUsernamePassword(file):
    import linecache 
    username=linecache.getline(file,1) #username on 1st line
    password=linecache.getline(file,2) #password on 2nd line
    return username.strip(),password.strip()  #remove the CRLF

import time
def ComputeFinishTime(sleep_time,resultcount):
    processingtime=0.15 #this may be processor/computer dependent, it took 5:10-->310s to process 300 address with a 0.75 sleep_time so 0.25 is reasonable for the dell precision 4300s 
    totalseconds=sleep_time*resultcount+processingtime*resultcount
    now=time.time() 
    endtime=time.strftime('%H:%M:%S' , (time.localtime(now+int(totalseconds))))

    print("This geocoding operation will take approximately %i seconds and complete at around %s." % (totalseconds,endtime))


def GeocodeDatabase(user,password):
    sleep_time = 0.15
    OverQueryLimitFlag = 0
    #the following line will need to change 
    con = mdb.connect('localhost', user, password, 'SheriffSales')
    with con:
        databasename=_Table
        cur = con.cursor(mdb.cursors.DictCursor)
        curUpdate = con.cursor(mdb.cursors.DictCursor)
        #for this database all records will need to be geocoded
        resultcount=int(cur.execute("SELECT id,LOCATION FROM %s WHERE Latitude is NULL"% (_Table)))
        print("Need to geocode "+str(resultcount)+" addresses.")
        rows = cur.fetchall()
        counter=0
        out_file_failed = _Outfile
        outf_failed = open(out_file_failed,'w')
        ComputeFinishTime(sleep_time,resultcount)        
        for row in rows:
            counter+=1
            print("Geocoding "+str(counter)+" of "+str(resultcount)+" addresses.")
            addr=row["LOCATION"]+"DAYTON OHIO"
            if OverQueryLimitFlag == 0:
                geocode_data=geocodeV2(addr) 
                if geocode_data['status']=="OK":
                    print(geocode_data)
                    lat=geocode_data['lat']
                    lon=geocode_data['lng']
                    curUpdate.execute("UPDATE %s SET Latitude=%s, Longitude=%s WHERE id=%s" % (_Table,lat,lon,row["id"]))  
                elif geocode_data['status']=="OVER_QUERY_LIMIT":
                    print("Over Query Limit Notification Received") 
                    OverQueryLimitFlag = 1
                else:
                    print("Geocoding of '"+row["LOCATION"]+"' failed with error code "+geocode_data['status'])
                    outf_failed.write(row["LOCATION"]+'\n')
                    outf_failed.flush()
            else:
                break
            time.sleep(sleep_time)  
        outf_failed.close()
    con.commit()
    cur.close()
    con.close()

#https://developers.google.com/maps/documentation/geocoding/
#root_url = "http://maps.google.com/maps/geo?"

root_url="http://maps.googleapis.com/maps/api/geocode/json?&address="
sensor_suffix="&sensor=false"
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


def geocodeV2(addr):
    values = {'address':addr,'sensor':'false'}
#py3    data = urllib.parse.urlencode(values)
    data = urllib.urlencode(values)
    root_url="http://maps.googleapis.com/maps/api/geocode/json?"
#py3    result=urllib.request.urlopen(root_url+data)
    result=urllib2.urlopen(urllib2.Request(root_url+data))

    content=result.read()
    decodedjson=json.loads(content.decode('utf-8'))
#    print(decodedjson)
    code=decodedjson['status']
    if code=="OK": #"SUCCESS": this changed from success to ok 
        outputlist = [s['geometry']['location'] for s in decodedjson['results']]
        #print(outputlist)
        first= outputlist[0]
        return { 'status':code,'lat':first['lat'],'lng':first['lng'] }
    else:
        return {'status':code}


########### MAIN ############
import sys
try:
    import MySQLdb as mdb #this module doesn't look like it'll ever be ported to py3, other modules available.  sudo pacman -S mysql-python
except ImportError:
    print("Module MySQLdb not found.")
    print("To install on Arch: sudo pacman -S mysql-python")
    print("Exiting.")
    sys.exit(1)
import urllib,urllib2,time,json

inputfilename=os.path.expanduser("~/.mysqllogin_rentalreg")
if len(sys.argv)>1 and sys.argv[1]!="":
    inputfilename=sys.argv[1]
else:
    print("No login file specified: GeocodeRentalRegistrationDatabase.py loginfile")
    print("using default file of %s" % (inputfilename))

if (not os.path.isfile(loginfile)):
    print("A valid loginfile was not provided.")
    print("Exiting.")
else:
    user,password=getUsernamePassword(inputfilename)
    GeocodeDatabase(user,password)
