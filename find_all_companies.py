#encoding:utf-8
import os
import pandas as pd

filePath=u'F:\新闻报道数据\媒体数据2000-2012'
result=[]
for foldername, subfoldername, filenames in os.walk(filePath):
    for file in filenames:
        if (file.endswith('.caj')):
            company=foldername.split('\\')[5]
            print(company)
            result.append([company,file])

pd.Dataframe(result).to_csv('result.csv')
