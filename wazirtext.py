
import requests
import random
import json
import hashlib
import hmac
import urllib
import uuid
import time as t
import copy
import math
import sys
from datetime import datetime
import calendar
import os
from requests_toolbelt import MultipartEncoder
from time import sleep
import os.path

from selenium import webdriver 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By 

# Turn off InsecureRequestWarning
# from requests.packages.urllib3.exceptions import InsecureRequestWarning
# requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Replace below path with the absolute path 
# to chromedriver in your computer 
driver = webdriver.Chrome('C:/chromedriver.exe') 
      
driver.get("https://web.whatsapp.com/") 
wait = WebDriverWait(driver, 600) 



API_URL = 'https://api.wazirx.com/api/v2/'

#x=requests.get(API_URL+"market-status")


def texting(target,string):         # Whatsapp Text Code
    print(string)                   # Remove the line if you do not want updates on your terminal
    x_arg = '//span[contains(@title,' + target + ')]'
    group_title = wait.until(EC.presence_of_element_located(( 
        By.XPATH, x_arg))) 
    group_title.click() 
    inp_xpath = '//div[@class="_2_1wd copyable-text selectable-text"][@dir="ltr"][@data-tab="6"]'
    input_box = wait.until(EC.presence_of_element_located(( 
        By.XPATH, inp_xpath))) 

    input_box.send_keys(string + Keys.ENTER)

data=[]

counter=0

while 1 :
    x=requests.get(API_URL+"tickers")
    a=x.content
    try:
        b=json.loads(a)
    except:
        continue
    #print("Data Loaded")
    l= len(b)
    head=[str("date")]
    x=datetime.fromtimestamp(b["btcinr"]['at'])
    #tt = t.localtime()
    #ct = t.strftime("%H:%M:%S", tt)
    row=[str(x)]
    openn=["Date_Place_holder"]
    for k,v in b.items():
        if (v['quote_unit'] == 'usdt' or v['quote_unit'] == 'inr'):
            head.append(str(v['name']))
            row.append(float(v['last']))
            openn.append(float(v['open']))
            #x=datetime.fromtimestamp(v['at'])
            #print(str(x)+" : "+v['name'] + "\t\t\t\t"+v['buy'] + "\t\t\t\t"+v['sell'] )        #if you want to print the buy/sell price of every coin or selective coins
    data.append(row)
    
    path='Stock.csv'
    
    string=""
    
    if counter>0:
        print(row,file=open("Stock.csv","a"))

        
    else :
        print(head,file=open("Stock.csv","a"))
        print(row,file=open("Stock.csv","a"))
    counter= counter+1
    print("Stock written to csv")
    if len(data)>=6:
        #print("Now greater than 5")
        for i in range(len(row)):
            if data[-1][i] != 0 and i!=0:
                ti=[]
                
                for j in range(-2,-6,-1):
                    if float(data[j][i]) ==0:
                        continue
                    tx=(float(data[-1][i]) - float(data[j][i]))/float(data[j][i]) *100
                    if tx >5 or tx <-5 :                # Defining First Change Alert Paramater
                        text= " down "
                        if tx>0:
                            text=" up "
                        for kk in range(j,-7,-1):
                            data[kk][i]=data[-1][i]
                        totaldiff = (float(data[-1][i]) - float(openn[i]))/float(openn[i]) *100
                        string= f"{head[i]} is {text} by {tx:.2f}% in last {-1-j} minute(s). Since Open 24hrs ago : {totaldiff:.2f}% & Now at : {data[-1][i]:.4f}"
                        if len(data) >7 and head[i]:
                            
                            print(string)
                            target = '""'               # Enter your Group name whcih will receive all updates regarding the first Paramater 
                            if tx>25 or tx <-25:        # Defining Second Change Alert Paramater
                                target1 = '""'          # Enter your Group name whcih will receive all updates regarding the Second Paramater 
                                texting(target1,string)
                            texting(target,string)
                        break;
    if counter%15==0:
         data=data[9:]
         
       
    
    tt = t.localtime()
    ct = t.strftime("%H:%M:%S", tt)

    print(f'At {ct} the Counter is {counter} : ')
    t.sleep(59)

