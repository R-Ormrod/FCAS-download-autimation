# -*- coding: utf-8 -*-
"""
Created on Wed Jun  1 15:55:20 2022

@author: Ryan O
"""

addedPath=r"C:\Users\Ryan O\Downloads\New\RAW FCAS Data\Already updated public prices\PUBLIC_PRICES_already ammended"
savePath = r"C:\Users\Ryan O\Downloads\New\RAW FCAS Data\New"
aggregated=r"C:\Users\Ryan O\Downloads\New\Temporary\FCAS_AggregationVIC1.csv"
# import requests
import zipfile, os
from bs4 import BeautifulSoup
import requests
from requests import get
from os.path import exists
from datetime import date, timedelta,datetime
today = date.today()

day=timedelta(1)
yesterday=today-day
yesterday=yesterday.strftime("%Y%m%d")
domain= "http://nemweb.com.au"
pre= '\PUBLIC_PRICES_'
suff = '.csv'
#####----------------------------------
f1 = open(aggregated, "r")
last_line = f1.readlines()[-1]
f1.close()
print(last_line)
time = last_line.split(",")[0]
time = datetime.strptime(time, "%d/%m/%Y %H:%M")
last_time=time-timedelta(days=1) #day before 4:00

##---------------------------------------------
# a="/Reports/Current/Public_Prices/PUBLIC_PRICES_202204020000_20220403040502.zip"
# b=a[45:72]
# 202204020000_20220403040502.zip

# full=addedPath+pre+'202205310000'
# file_exists = exists(full)
# with requests.Session() as s:
#     download = s.get(CSV_URL)

#     decoded_content = download.content.decode('utf-8')

#     cr = csv.reader(decoded_content.splitlines(), delimiter=',')
#     my_list = list(cr)
#     for row in my_list:
#         print(row)


page = requests.get(('http://nemweb.com.au/Reports/Current/Public_Prices/'))
filetype = '.zip'
soup = BeautifulSoup(page.text, 'html.parser')

for link in soup.find_all('a'):
    url = link.get('href')
    if filetype in url:
        print(url)
        filename=url[45:72]
        filename2=url[45:53]
        date_time_test = datetime.strptime(filename2, "%Y%m%d")

        # if exists(addedPath+pre+filename+'.csv'):
        #     print('file Exists')
        #     print(filename2)
        if (date_time_test<last_time):
            print(filename2+"included already")   
        else:
            print('Downloading...',end="\r")
            fileName=url[31:]
            with open(fileName, 'wb') as file:
                response = get(domain+url)
                file.write(response.content)
                print('...Complete')     
    else:
        continue

working_directory = os.getcwd()
#os.chdir(working_directory)

for file in os.listdir(working_directory):   # get the list of files
    if zipfile.is_zipfile(file): # if it is a zipfile, extract it
        file_name = os.path.abspath(file)
        # print(file_name)
        with zipfile.ZipFile(file) as item: # treat the file as a zip
            item.extractall()  # extract it in the working directory
            item.close()
            os.remove(file_name) # delete zipped file