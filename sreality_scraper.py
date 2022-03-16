
from math import ceil
import os
from tkinter import Image
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
import pandas as pd
import numpy as np
from PIL import Image
import time
import sys
#import requests
#from bs4 import BeautifulSoup

PATH = os.path.dirname(os.path.abspath(__file__))
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')  # Last I checked this was necessary.
options.add_experimental_option("excludeSwitches", ["enable-logging"])
try:
     ser = Service(sys._MEIPASS + '\\msedgedriver.exe')
except:
    ser = Service(PATH + '\\msedgedriver.exe')
driver = webdriver.Edge(options = options, service= ser )
driver.implicitly_wait(10)
url = 'https://www.sreality.cz/hledani/pronajem/komercni/kancelare/praha-7,praha-8'
while True:
    url = input("Please enter a valid sreality search url: \n")

    try:
        driver.get(url)
        try:
            all_listings = int(driver.find_element(By.XPATH, "//descendant::span[@class = 'numero ng-binding'][2]").text)
        except:
            all_listings = len(driver.find_elements(By.XPATH, ("//*[@class='property ng-scope']"))) -1
        no_of_pages = ceil(all_listings/20)
#ids = driver.find_elements(By.XPATH, ('//*[@id]')
    
#ids = driver.find_elements(By.XPATH, ('//html/body/div[2]/div[1]/div[2]/div[3]/div[3]/div/div/div/div/div[3]/div/child::*') 
#ids = [ii for ii in ids if ii.get_attribute('class') == 'property ng-scope' ] 
    except:
        msg = "Invalid url given: url needs to look something like 'https://www.sreality.cz/hledani/pronajem/komercni/kancelare/praha-7,praha-8'"
        print(msg)
        continue
    else:
        break



print('Scraping...')
print(str(no_of_pages) + ' pages found with given search criteria, '+ str(all_listings) + ' properties in total...')
try:
    os.mkdir(PATH + '\\screenshots') 
except:
    pass
pd.set_option('display.max_colwidth', None )
property_data = pd.DataFrame(columns= ['location', 'area', 'rent','rent per sqm', 'link'])
for page in range(1,no_of_pages+1):
    if page>1:
        page_url = url +'&strana=' + str(page)
        driver.get(page_url)
    listings = driver.find_elements(By.XPATH, ("//*[@class='property ng-scope']"))
    loc = listings[-1].location
    size = listings[-1].size
    x = loc['x'];
    y = loc['y'];
    width = loc['x']+size['width'];
    height = loc['y']+size['height'];
    driver.set_window_size(width,height)
    time.sleep(0.5)
    no_of_listings_on_page = len(listings)
    listings = listings[1:len(listings)]
    for property in listings:   
        try:
            location = property.find_element(By.XPATH, ".//descendant::span[@class = 'locality ng-binding']").text
            link = property.find_element(By.XPATH,".//descendant::a").get_attribute('href')
            area = property.find_element(By.XPATH,".//descendant::span[@class='name ng-binding']").text
            area = area[0:len(area)-2]
            area = int(''.join([c for c in area if c.isdigit()]))
            price = property.find_element(By.XPATH,".//descendant::span[@class='norm-price ng-binding']").text
            price = int(''.join([c for c in price if c.isdigit()])) 
            rent_per_sqm = price/area
            #to_be_screenshotted = driver.find_element(By.XPATH, "//descendant::div[@class='property-detail ng-scope']" )
            property.screenshot(PATH + '\\screenshots\\' + location + ' '+ str(area)+ 'm2 '  + str(price) + ' Kc.png')
            im = Image.open(PATH + '\\screenshots\\' + location + ' '+ str(area)+ 'm2 ' + str(price) + ' Kc.png')
            im.thumbnail((450,170), Image.LANCZOS)
            im.save(PATH + '\\screenshots\\' + location + ' '+ str(area)+ 'm2 ' + str(price) + ' Kc.png')
            if not ((property_data['location'] == location) & (property_data['rent per sqm'].apply(np.round) == np.round(rent_per_sqm) )).any():
                new_data = pd.DataFrame.from_dict({'location': [location], 'area': [area], 'rent': [price], 'rent per sqm': [rent_per_sqm], 'link': [link]})
                property_data = pd.concat([property_data,new_data], ignore_index=True)
        except Exception:
            continue
    print('Finished page ' +str(page)+ ' of ' + str(no_of_pages)+ '...')
    # for i in range(1,no_of_listings_on_page):
    # #property = WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH, "//*[@class='property ng-scope']")))[i]
    #     try:

    #         property = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//descendant::a[@class='title']["+ str(i+1) +"]")))
    #         property.click()        


    #         location = driver.find_element(By.XPATH, "//descendant::span[@class='location-text ng-binding']").text
    #         link = driver.current_url

            



    #         params1 = driver.find_elements(By.XPATH, "//*[@class='params1']")[0]
    #         params2 = driver.find_elements(By.XPATH, "//*[@class='params2']")[0]

    #         try:
    #             price = params1.find_element(By.XPATH,".//label[contains(text(),'Celková cena')]/following-sibling::strong/*[1]").text 
    #             price = price.replace(' ', '')
    #             price = int(price[:price.find('Kč')])
    #         except:
    #             try:
    #                 price = params1.find_element(By.XPATH,".//label[contains(text(),'Zlevněno')]/following-sibling::strong/*[1]").text 
    #                 price = price.replace(' ', '')
    #                 price = int(price[:price.find('Kč')])
    #             except:
    #                 try:
    #                     price = params2.find_element(By.XPATH,".//label[contains(text(),'Celková cena')]/following-sibling::strong/*[1]").text 
    #                     price = price.replace(' ', '')
    #                     price = int(price[:price.find('Kč')])
    #                 except:
    #                     try:
    #                         price = params2.find_element(By.XPATH,".//label[contains(text(),'Zlevněno')]/following-sibling::strong/*[1]").text  
    #                         price = price.replace(' ', '')
    #                         price = int(price[:price.find('Kč')])
    #                     except:
    #                         price = 0


    #         try:
    #             area = params2.find_element(By.XPATH,".//label[contains(text(),'Užitná plocha')]/following-sibling::strong/*[1]").text 
    #             area = area.replace(' ', '')
    #             area = int(area)
    #         except:
    #             area = params1.find_element(By.XPATH,".//label[contains(text(),'Užitná plocha')]/following-sibling::strong/*[1]").text
    #             area = area.replace(' ', '')
    #             area = int(area)
            
    #         element = driver.find_element(By.XPATH, "//descendant::div[@class='property-detail ng-scope']")
    #         loc = element.location;
    #         size = element.size;
    #         WebDriverWait(driver,20).until(EC.visibility_of_element_located((By.XPATH, "//descendant::div[@class='property-detail ng-scope']" )))
             

    #         x = loc['x'];
    #         y = loc['y'];
    #         width = loc['x']+size['width'];
    #         height = loc['y']+size['height'];
    #         driver.set_window_size(width,height)
    #         driver.save_screenshot('pageImage.png');  
    #         im = Image.open('pageImage.png')
    #         im = im.crop((int(x), int(y), int(width), int(height)))
    #         im.save(PATH + '\\kancelare\\' + location + '.png')

    #         property_data = property_data.append({'location': location, 'area':area, 'rent': price, 'link': link} , ignore_index= True)
    #         driver.back()
    #     except:
    #         continue

    #ids = driver.find_elements(By.XPATH, ('//html/body/div[2]/div[1]/div[2]/div[3]/div[3]/div/div/div/div/div[3]/div/child::*') 
    #ids = [ii for ii in ids if ii.get_attribute('class') == 'property ng-scope' ]   # get all property listing elements
    #ids = driver.find_elements_by_class_name('property ng-scope')
    #ids = [ii.find_elements('xpath', './/*') for ii in ids]

property_data['image'] = property_data.apply(lambda row:  PATH + '\\screenshots\\' + row.location + ' '+ str(row.area)+ 'm2 ' + str(row.rent) + ' Kc.png' , axis =1)

#property_data.to_html('property_data.html', formatters={'image': image_formatter}, escape=False )
print( str(len(property_data.index)) + ' properties found with prices publicly listed, saving data...')
writer = pd.ExcelWriter('property_data.xlsx', engine='xlsxwriter')
property_data.rename(columns ={'area': 'area, in sqm'}, inplace= True)
property_data[['location', 'area, in sqm', 'rent', 'rent per sqm', 'link']].to_excel(writer, sheet_name='Sheet1')
workbook = writer.book
worksheet = writer.sheets['Sheet1']
worksheet.set_column_pixels(6,6,455)
property_data['link'].map(lambda x: len(x)).max()
for i in range(1,6):
    worksheet.set_column(i,i,property_data.iloc[:,i-1].map(lambda x: len(str(x))).max()+5)
worksheet.write(0,6,'image')
for i in range(len(property_data['image'])):
    worksheet.set_row_pixels(i+1,175)
    worksheet.insert_image('G'+ str(i+2), property_data['image'][i])
driver.close()
writer.save()
print('Data saved to property_data.xlsx')
sys.exit()

#/html/body/div[2]/div[1]/div[2]/div[3]/div[3]/div/div/div/div/div[3]/div/div[2]
#/html/body/div[2]/div[1]/div[2]/div[3]/div[3]/div/div/div/div/div[3]/div/div[3]
#/html/body/div[2]/div[1]/div[2]/div[3]/div[3]/div/div/div/div/div[3]/div/div[3]/div/div/span/span[2]/span[1]