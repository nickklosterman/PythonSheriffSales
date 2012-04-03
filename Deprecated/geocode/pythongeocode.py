#taken from http://snipplr.com/view/15270/python-geocode-address-via-urllib/
import urllib,urllib2,time
addr_file = 'addresses.csv'
out_file = 'addresses_geocoded.csv'
out_file_failed = 'failed.csv'
sleep_time = 2
root_url = "http://maps.google.com/maps/geo?"
gkey = "YourGoogleKeyGoesHere"
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
    values = {'q' : addr, 'output':out_fmt, 'key':gkey}
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
def main():
    #open our i/o files
    outf = open(out_file,'w')
    outf_failed = open(out_file_failed,'w')
    inf = open(addr_file,'r')
    for address in inf:
    #get latitude and longitude of address
        data = geocode(address)
    #output results and log to file
        if len(data)>1:
            print "Latitude and Longitude of "+address+":"
            print "\tLatitude:",data['lat']
            print "\tLongitude:",data['lng']
            outf.write(address.strip()+data['lat']+','+data['lng']+'\n')
            outf.flush()
        else:
            print "Geocoding of '"+addr+"' failed with error code "+data['code']
            outf_failed.write(address)
            outf_failed.flush()
    #play nice and don't just pound the server with requests
        time.sleep(sleep_time)
    #clean up
    inf.close()
    outf.close()
    outf_failed.close()
if __name__ == "__main__":
    main()
