import urllib,urllib2,json
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
#    print(decodedjson)    
    if code == "OK":
        outputlist = [s['geometry']['location'] for s in decodedjson['results']]
        first= outputlist[0]
        return { 'status':code,'lat':first['lat'],'lng':first['lng'] }
    else:
        return { 'status':code }

