
import urllib,urllib2,time,json
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
    code=decodedjson['status']
    if code =="OK":    
        outputlist = [s['geometry']['location'] for s in decodedjson['results']]
        first= outputlist[0]
        return { 'status':code,'lat':first['lat'],'lng':first['lng'] }
    else:
        return { 'status':code }

