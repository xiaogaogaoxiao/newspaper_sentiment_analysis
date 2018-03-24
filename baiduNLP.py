# coding:gbk
import urllib, urllib2, sys
import requests
import ssl
import json
import time

def baidu(data):
    url = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify?access_token=24.24caa83c34e5d01f2e5fb80752adae8c.2592000.1522201224.282335-10469707'
    post_data = "{\"text\":\"" + data + "\"}"
    request = urllib2.Request(url, post_data)
    request.add_header('Content-Type', 'application/json')
    try:
        response = urllib2.urlopen(request)
        content = response.read()
        content2=json.loads(content.decode('gbk'))
        if (content.find('\"error_msg\"') == -1):
            content2=content2['items'][0]
            return content2['positive_prob'],content2['negative_prob'],content2['confidence'],content2['sentiment']
        else:
            print content2
            return 0,0,0,0
    except:
        return 0,0,0,0
