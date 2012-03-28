#taken from http://snipplr.com/view/15270/python-geocode-address-via-urllib/
import urllib,urllib2,time,sys
addr_file = 'output.txt'
out_file = 'output_geocoded.txt'
out_file_failed = 'output_failed.txt'
sleep_time = 2
root_url = "http://maps.google.com/maps/geo?"
gkey = "YourGoogleKeyGoesHere" #no longer required as far as I can tell 3-28-2012
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
    address=sys.argv[1]
    print(address)
    #get latitude and longitude of address
    geocode_data = geocode(address)
    #output results and log to file
    if len(geocode_data)>1:
        print "Latitude and Longitude of "+address+":"
        print "\tLatitude:",geocode_data['lat']
        print "\tLongitude:",geocode_data['lng']
    else:
        print "Geocoding of '"+address+"' failed with error code "+geocode_data['code']
        
if __name__ == "__main__":
    main()
