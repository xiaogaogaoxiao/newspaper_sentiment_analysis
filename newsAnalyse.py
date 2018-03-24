# coding:utf-8
import os
import codecs
import baiduNLP
import csv
import chardet



def decide(companyName,title,text):
    companyName=companyName.strip('*')
    companyName = companyName.strip('ST')
    companyName=companyName.strip(u'原')
    companyName = companyName.strip(u'股份')
    companyName = companyName.strip(u'公路股份有限公司')
    companyName = companyName.strip(u'国际')
    companyName = companyName.strip(u'A')
    companyName = companyName.strip(u'健康')
    companyName = companyName.strip(u'华润')
    companyName = companyName.strip(u'物流')
    companyName = companyName.strip(u'能源')
    companyName = companyName.strip(u'投资')
    companyName = companyName.strip(u'科技')
    companyName = companyName.strip(u'路机')
    companyName = companyName.strip(u'酒业')
    title=title.strip('_')
    if (title.find(companyName) != -1):
        return 1
    elif (title.find(companyName) == -1 and (title.find(u'大盘') != -1 or title.find(u'板块') != -1) and (
        text.find(companyName) != -1)):
        return 0.5
    elif (title.find(companyName) == -1 and title.find(u'大盘') == -1 and title.find(u'板块') == -1):
        num = text.count(companyName)
        if num > 1:
            return 1
        elif num == 1:
            return 0.25
        else:
            return 0

def preProcess(foldername,file):
    print('Now you are dealing with:')
    company=foldername.split('\\')[4]
    filename = file
    foldername = foldername
    fileLocation =os.path.join(foldername,filename)
    print(filename)

    text = codecs.open(fileLocation.replace('\\', '/')).read()
    if text[:3]==codecs.BOM_UTF8:
        text=text[3:]
    text=text.decode(chardet.detect(text)['encoding'])
    filename=filename.replace('+','')
    filename = filename.replace('=', '')
    filename = filename.replace('-', '')
    text = ''.join(text.split())
    return [filename,company,text]
    # except:
    #     return ['fail', 'fail', '']

def preProcess2(foldername,file):
    print('Now you are dealing with:')
    company=''
    filename = file.encode('gbk')
    foldername = foldername.encode('gbk')
    fileLocation = foldername + '/' + filename
    print os.path.join(foldername,filename)
    try:
        text = codecs.open(fileLocation.replace('\\', '/')).read()
        if text[:3] == codecs.BOM_UTF8:
            text = text[3:]
        text = text.decode(chardet.detect(text)['encoding'])
        filename=filename.replace('+','')
        filename = filename.replace('=', '')
        filename = filename.replace('-', '')
        text = ''.join(text.split())
        return [filename,company,text]
    except:
        print 'preProcessFail'
        return ['fail', 'fail', '']

def getDate(text):
    text0=text.split('/')
    try:
        date=text0[1]+text0[2]+text0[3]
        return [text0[0],date]
    except:
        return ['0','0']

def tooLong(text):
    length=len(text)
    flag=0
    fraction = min(length, 900)
    [positive_prob, negative_prob, confidence, sentiment] = baiduNLP.baidu(text[:fraction].encode('gbk', 'replace'))
    positive_prob_sum=positive_prob*2
    negative_prob_sum=negative_prob*2
    confidence_sum=confidence*2
    s=2

    while(flag+fraction<length):
        flag=flag+fraction
        [positive_prob, negative_prob, confidence, sentiment] = baiduNLP.baidu(text[flag:flag+fraction].encode('gbk', 'replace'))
        positive_prob_sum = positive_prob+positive_prob_sum
        negative_prob_sum = negative_prob+negative_prob_sum
        confidence_sum = confidence+confidence_sum
        s=s+1

    [positive_prob, negative_prob, confidence, sentiment] = baiduNLP.baidu(text[flag:].encode('gbk', 'replace'))
    positive_prob_sum = positive_prob + positive_prob_sum
    negative_prob_sum = negative_prob + negative_prob_sum
    confidence_sum = confidence + confidence_sum
    s = s + 1

    positive_prob=positive_prob_sum/s
    if (positive_prob > 0.525):
        sentiment = 2
    elif (positive_prob < 0.475):
        sentiment = 0
    else:
        sentiment = 1
    return [positive_prob,1-positive_prob,confidence_sum/s,sentiment]

if __name__=="__main__":
    loc=u'19-50 caj to txt 2'
    filePath=u'F:\\新闻报道补充\\'+loc
    foldername = []
    subfoldername = []
    filenames = []
    filenames = os.listdir(filePath)
    outputfile=open(loc+'.csv','w')
    outputWriter=csv.writer(outputfile)
    num=0
    for foldername, subfoldername, filenames in os.walk(filePath):
        for file in filenames:
            if(file.endswith('.txt')):
                [filename,company,text]=preProcess2(foldername,file)
                if(filename!='fail'):
                    [magazine,time]=getDate(text)
                    if(len(text)>1000):
                        [positive_prob, negative_prob, confidence, sentiment]=tooLong(text)
                    else:
                        [positive_prob, negative_prob, confidence, sentiment] = baiduNLP.baidu(text.encode('gbk','replace'))
                    try:
                        result=[positive_prob, negative_prob, confidence, sentiment,file.replace('.txt','').encode('utf-8','replace'),company.encode('utf-8','replace'),magazine.encode('utf-8','replace'),time.encode('utf-8','replace'),text.encode('utf-8','replace'),decide(company,file.replace('.txt',''),text)]
                        outputWriter.writerow(result)
                        num=num+1
                        print(num)
                    except:
                        result = [0,0,0,3,file.replace('.txt', '').encode('utf-8', 'replace'), 0,0,0,foldername.encode('utf-8', 'replace'),decide(company,file.replace('.txt',''),text)]
                        outputWriter.writerow(result)
                        num = num + 1
                        print(num)
                        print("wrong")
                else:
                    result = [0, 0, 0, 3, file.replace('.txt', '').encode('utf-8', 'replace'), 0, 0, 0,
                              foldername.encode('utf-8', 'replace'),decide(company,file.replace('.txt',''),text)]
                    outputWriter.writerow(result)
                    num = num + 1
                    print(num)
                    print "can't_open"
    outputfile.close()

