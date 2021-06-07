import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities  
from selenium.webdriver.common.action_chains import ActionChains  

capabilities = DesiredCapabilities.CHROME
capabilities['loggingPrefs'] = { 'browser':'ALL' }


vehicles_df = pd.read_csv('vehicles.csv')
cost_vehicle = []
cost_fuel =[]
cost_maintenance =[]

emit_vehicleprod =[]
emit_batteryprod = []
emit_fuelprod =[]
emit_fuelcons = []

vehs_data=[]



driver = webdriver.Chrome(executable_path=r"C:\Users\Thomas Berger\Downloads\chromedriver_win32(1)\chromedriver.exe",desired_capabilities=capabilities)
for i in vehicles_df.VehicleId:
    driver.get('https://www.carboncounter.com/#!/details?cars='+ str(i))
    action = ActionChains(driver)
    veh_Data=[]
    for k,j in enumerate(['#bar-group-costs_veh_monthly','#bar-group-costs_fuel_monthly','#bar-group-costs_maintenance_monthly',
              '#bar-group-ghg_veh','#bar-group-ghg_batt','#bar-group-ghg_fuel_prod','#bar-group-ghg_fuel_op']):
        
        point = driver.find_element_by_css_selector(j)
        action.reset_actions()
        action.move_to_element(point).perform()
        tooltip = driver.find_elements_by_id("tooltip-firstline")
        txt = tooltip[-1].text
        if k<=2:
            nb = float(txt.replace(" US$ / month", ""))
        else:
            nb = txt.replace(" gCO₂eq / mile", "")
            if nb == '':
                nb= np.nan
            else:
                nb=float(nb)
        veh_Data.append(nb)
    vehs_data.append(veh_Data)

#%%
vehics = np.array(vehs_data)
vehicles_df['cost_vehicle'] = vehics[:,0]

vehicles_df['cost_fuel'] = vehics[:,1]

vehicles_df['cost_maintenance'] = vehics[:,2]

vehicles_df['emit_vehicleprod'] = vehics[:,3]

vehicles_df['emit_batteryprod'] = vehics[:,4]

vehicles_df['emit_fuelprod'] = vehics[:,5]

vehicles_df['emit_fuelcons'] = vehics[:,6]

#%%
vehicles_df.to_csv('vehicles.csv',index=False)