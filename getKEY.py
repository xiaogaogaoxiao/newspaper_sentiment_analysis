import urllib, urllib2, sys
import ssl


host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=njhvo8igfDVtlbQ0g3l1HdeG&client_secret=k4cu5w4ppbSwngGpG7YmN35NaTKaUHRg'
request = urllib2.Request(host)
request.add_header('Content-Type', 'application/json; charset=UTF-8')
response = urllib2.urlopen(request)
content = response.read()
if (content):
    print(content)