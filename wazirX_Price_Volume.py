
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
import threading
import pandas as pd
from selenium import webdriver 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By 

#import pyautogui as pp

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
    inp_xpath = '//div[contains(@class,"copyable-text selectable-text")][@dir="ltr"][@data-tab="9"]'
    input_box = wait.until(EC.presence_of_element_located(( 
        By.XPATH, inp_xpath))) 
    #pp.FAILSAFE=False
    input_box.send_keys(string + Keys.ENTER)
    # pp.typewrite(string)
    # pp.press('enter')


# for i in range(l):
    # if b['markets'][i]['quote_unit'] == 'usdt' and b['markets'][i]['status'] == 'active' and 'buy' in b['markets'][i].keys() :
        # print(b['markets'][i]['baseMarket'] +"/" +b['markets'][i]['quoteMarket'] +"\t:\t\t"+b['markets'][i]['buy'] + "  \t::\t  " +b['markets'][i]['sell'])



#print(l)



def wazirt():
    data=[]
    vold=[]

    counter=0
    # target = '"Crypto Updates"'
    # string = "./startv2"
    # texting(target,string)
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
        vol=[str(x)]

        openn=["Date_Place_holder"]
        for k,v in b.items():
            if (v['quote_unit'] == 'usdt'):
                head.append(str(v['name']))
                row.append(float(v['last']))
                vol.append(float(v['volume']))
                openn.append(float(v['open']))
                #x=datetime.fromtimestamp(v['at'])
                #print(str(x)+" : "+v['name'] + "\t\t\t\t"+v['buy'] + "\t\t\t\t"+v['sell'] )
        data.append(row)
        vold.append(vol)
        
        path='Stockvol.csv'
        #print("Stock Parsed")
        string=""
        
        if counter>0:
            #print(row)
            print(row,file=open("Stockvol.csv","a"))
            #file.close()
            
        else :
            #print(head)
            print(head,file=open("Stockvol.csv","a"))
            #print(row)
            #file.close()
            print(row,file=open("Stockvol.csv","a"))
            #file.close()
        # print("Stock written to csv")\
        
        path='vol.csv'
        #print("Stock Parsed")
        string=""
        
        if counter>0:
            #print(row)
            print(vol,file=open("vol.csv","a"))
            #file.close()
            
        else :
            #print(head)
            print(head,file=open("vol.csv","a"))
            #print(row)
            #file.close()
            print(vol,file=open("vol.csv","a"))
            #file.close()
        # print("Stock written to csv")
        counter= counter+1
        tx=0
        if len(data)>=6:
            #print("Now greater than 5")
            for i in range(len(row)):
                if data[-1][i] != 0 and i!=0:
                    ti=[]
                    
                    for j in range(-2,-6,-1):
                        if float(data[j][i]) ==0:
                            continue
                        tx=(float(data[-1][i]) - float(data[j][i]))/float(data[j][i]) *100
                        if tx >5 or tx <-5 :        # Defining First Change Alert Paramater
                            text= " down "
                            if tx>0:
                                text=" up "
                            for kk in range(j,-7,-1):
                                data[kk][i]=data[-1][i]
                            totaldiff = (float(data[-1][i]) - float(openn[i]))/float(openn[i]) *100
                            string= f"{head[i]} is {text} by {tx:.2f}% in last {-1-j} minute(s). Since Open 24hrs ago : {totaldiff:.2f}% & Now at : {data[-1][i]:.4f}"
                            print(string)
                            if len(data) >7 and head[i]:
                                print(string)
                                target = '""'               # Enter your Group name whcih will receive all updates regarding the first Paramater 
                                if tx>25 or tx <-25:        # Defining Second Change Alert Paramater
                                    target1 = '""'          # Enter your Group name whcih will receive all updates regarding the Second Paramater 
                                    texting(target1,string)
                                texting(target,string)
                            break;
            if (tx >1 or tx <-1) and string!="" :
                print(string)
        tx=0
        string=""
        if len(vold)>=6:
            #print("Now greater than 5")
            for i in range(len(row)):
                if vold[-1][i] != 0 and i!=0:
                    ti=[]
                    
                    for j in range(-2,-6,-1):
                        if float(vold[j][i]) ==0:
                            continue
                        tx=(float(vold[-1][i]) - float(vold[j][i]))/float(vold[j][i]) *100
                        if tx >10 or tx <-10 :              # Defining First Change Alert Paramater
                            text= " decreased "
                            if tx>0:
                                text=" increased "
                            for kk in range(j,-7,-1):
                                vold[kk][i]=vold[-1][i]
                            # totaldiff = (float(vold[-1][i]) - float(openn[i]))/float(openn[i]) *100
                            string= f"{head[i]} volume has {text} by {tx:.2f}% in last {-1-j} minute(s). Now at : {vold[-1][i]:.4f}"
                            print(string)
                            if len(vold) >7 and head[i]:
                                print(string)
                                target = '""'               # Enter your Group name whcih will receive all updates regarding the first Paramater 
                                if tx>50 or tx <-50:        # Defining Second Change Alert Paramater
                                    target1 = '""'          # Enter your Group name whcih will receive all updates regarding the Second Paramater 
                                    texting(target1,string)
                                texting(target,string)
                            break;
            if (tx >1 or tx <-1) and string!="" :
                print(string)
        #print("Before counter")
        if counter%15==0:
            #counter=0
            data=data[9:]
            vold=vold[9:]

            #print("Inside counter")
        tt = t.localtime()
        ct = t.strftime("%H:%M:%S", tt)
        #pp.FAILSAFE=False
        #pp.click(500,250)
        print(f'At {ct} the Counter is {counter} : ')
        t.sleep(59)
        #print(b)




y = threading.Thread(target=wazirt)
y.daemon=True
y.start()

print("before while")
while input()!="stop":
    continue
driver.close()
sys.exit()