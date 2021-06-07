import numpy as np
import csv
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities  
from selenium.webdriver.common.action_chains import ActionChains  

capabilities = DesiredCapabilities.CHROME
capabilities['loggingPrefs'] = { 'browser':'ALL' }

driver = webdriver.Chrome(executable_path=r"C:\Users\Thomas Berger\Downloads\chromedriver_win32(1)\chromedriver.exe",desired_capabilities=capabilities)


lists = np.arange(34000,37000)
yes = []


for i in lists:
    driver.get('https://www.carboncounter.com/#!/explore?cars='+ str(i))
    
# print console log messages
    if len(driver.get_log('browser'))==0:
        yes.append(i)
        
driver.close() 

with open('yes.csv', 'w') as f:
      
    # using csv.writer method from CSV package
    write = csv.writer(f)
      
    write.writerow(yes)