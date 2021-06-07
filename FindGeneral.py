import numpy as np
import csv
import re

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities  
from selenium.webdriver.common.action_chains import ActionChains  

capabilities = DesiredCapabilities.CHROME
capabilities['loggingPrefs'] = { 'browser':'ALL' }

with open('yes.csv') as f:
    reader = csv.reader(f)
    yes = list(reader)[0]

vehicles = []


for i in yes:
    driver = webdriver.Chrome(executable_path=r"C:\Users\Thomas Berger\Downloads\chromedriver_win32(1)\chromedriver.exe",desired_capabilities=capabilities)
    driver.get('https://www.carboncounter.com/#!/explore?cars='+ str(i))
    action = ActionChains(driver)
    point = driver.find_elements_by_css_selector(".dataPoint.highlight")
    action.move_to_element(point[-1]).perform()
    
    
    tooltip = driver.find_element_by_id("tooltip")
    tooltiptxt = tooltip.text
    tooltiptxt = tooltiptxt.split('\n')
    data = tooltiptxt[1].split(' | ')
    
    split = data[0].split(" ")
    if len(split) ==5:
        mpge=split[0]
        mpg=split[3]
    elif split[1]=='MPGe':
        mpge=split[0]
        mpg=-1
    else:
        mpge=-1
        mpg=split[0]
        
    vehicles.append([i,tooltiptxt[0],mpge,mpg,float(data[1].replace(" HP", "")),data[2]])
    driver.close()
    
    # %%
import pandas as pd

vehicles_df = pd.DataFrame(np.array(vehicles), columns = [ "VehicleId","brand + Model", "MPGe","MPG", "HP", "drivetrain"])
vehicles_df.to_csv('vehicles.csv',index=False)

# %%
vehicles_df = pd.read_csv('vehicles.csv')