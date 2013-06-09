#this program geocodes a database
from geocodeV2 import geocodeV2

import time
def ComputeFinishTime(sleep_time,resultcount):
    processingtime=0.25 #this may be processor/computer dependent, it took 5:10-->310s to process 300 address with a 0.75 sleep_time so 0.25 is reasonable for the dell precision 4300s 
    totalseconds=sleep_time*resultcount+processingtime*resultcount
    now=time.time() 
    endtime=time.strftime('%H:%M:%S' , (time.localtime(now+int(totalseconds))))

    print("This geocoding operation will take approximately %i seconds and complete at around %s." % (totalseconds,endtime))

def GeocodeDatabase(user,password):
    sleep_time = 0.75
    con = mdb.connect('localhost', user, password, 'SheriffSales')
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        curUpdate = con.cursor(mdb.cursors.DictCursor)
        resultcount=int(cur.execute("SELECT id,Address FROM Property WHERE Latitude is NULL"))
        print("Need to geocode "+str(resultcount)+" addresses.")
        rows = cur.fetchall()
        counter=0
        out_file_failed = 'geocode_failed.txt'
        outf_failed = open(out_file_failed,'w')
        ComputeFinishTime(sleep_time,resultcount)
        for row in rows:
            counter+=1
            print("Geocoding "+str(counter)+" of "+str(resultcount)+" addresses.")
#            ComputeFinishTime(sleep_time,resultcount)
            if 1==1:
                print(row["Address"])
                geocode_data=geocodeV2(row["Address"])
                #if len(geocode_data)>1:
                if geocode_data['status']=="OK":
                    lat=geocode_data['lat']
                    lon=geocode_data['lng']
                    curUpdate.execute("UPDATE Property SET Latitude=%s, Longitude=%s WHERE id=%s", (lat,lon,row["id"]))  #SELECT count(*) FROM Property WHERE Latitude is NULL 
                else:
                    print("Geocoding of '"+row["Address"]+"' failed with error code "+geocode_data['status'])
                    outf_failed.write(row["Address"]+'\n')
                    outf_failed.flush()
                time.sleep(sleep_time)  
        outf_failed.close()
    con.commit()
    cur.close()
    con.close()

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


#NOTE used anymore. we use the geocodeV2.py module that is in the same directory.
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

def getUsernamePassword(file):
    import linecache
    username=linecache.getline(file,1) #username on 1st line
    password=linecache.getline(file,2) #password on 2nd line
    return username.strip(),password.strip()  #remove the CRLF   

########### MAIN ############

import sys
import MySQLdb as mdb
import urllib,urllib2,time

#check if argv[1]!=null and assign to 
#if sys.argv[#

inputfilename="/home/nicolae/.mysqllogin"
if len(sys.argv)>1 and  sys.argv[1]!="":
    inputfilename=sys.argv[1]
else:
    print("No login file: GeocodeDatabase.py loginfile")
    print("using default file of %s" % (inputfilename))

user,password=getUsernamePassword(inputfilename)
GeocodeDatabase(user,password)





