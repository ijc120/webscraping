from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from datetime import date
import time
import re
import csv
from bs4 import BeautifulSoup

driver = webdriver.Chrome()
driver.get("https://www.sephora.com/brands-list")
brand_pages = driver.find_elements_by_xpath("//a[@class='css-ezuahi ']")
product_list=[]
brands = ['https://www.sephora.com/brand/acqua-di-parma','https://www.sephora.com/brand/algenist','https://www.sephora.com/brand/benefit-cosmetics','https://www.sephora.com/brand/boscia','https://www.sephora.com/brand/bobbi-brown','https://www.sephora.com/brand/burberry','https://www.sephora.com/brand/bvlgari','https://www.sephora.com/brand/chanel','https://www.sephora.com/brand/chloe','https://www.sephora.com/brand/clarins','https://www.sephora.com/brand/clarisonic','https://www.sephora.com/brand/clinique','https://www.sephora.com/brand/dior','https://www.sephora.com/brand/dolce-gabbana','https://www.sephora.com/brand/dr-jart','https://www.sephora.com/brand/estee-lauder','https://www.sephora.com/brand/eve-lom','https://www.sephora.com/brand/fresh','https://www.sephora.com/brand/giorgio-armani-beauty','https://www.sephora.com/brand/givenchy','https://www.sephora.com/brand/glamglow','https://www.sephora.com/brand/gucci','https://www.sephora.com/brand/guerlain','https://www.sephora.com/brand/jo-malone-london','https://www.sephora.com/brand/l-occitane','https://www.sephora.com/brand/la-mer','https://www.sephora.com/brand/lancome','https://www.sephora.com/brand/laneige','https://www.sephora.com/brand/make-up-for-ever','https://www.sephora.com/brand/michael-kors','https://www.sephora.com/brand/miu-miu','https://www.sephora.com/brand/nars','https://www.sephora.com/brand/origins','https://www.sephora.com/brand/peter-thomas-roth','https://www.sephora.com/brand/philosophy','https://www.sephora.com/brand/prada','https://www.sephora.com/brand/rossano-ferretti-parma','https://www.sephora.com/brand/shiseido','https://www.sephora.com/brand/sephora-collection','https://www.sephora.com/brand/sk-ii','https://www.sephora.com/brand/tom-ford','https://www.sephora.com/brand/viktor-rolf','https://www.sephora.com/brand/yves-saint-laurent']

for brand in brands:
    driver.get(brand)   

    a=driver.find_element_by_partial_link_text('See All').get_attribute('href')
    driver.get(a)
    product_number= driver.find_element_by_xpath("//span[@data-at='number_of_products']").text

    number = int(product_number.split(' ')[0])
    print(number)
    page = int(number/60)
    print(page)

    total_products=[]

    for n in range(page +1):   
        for j in range(10):
            driver.execute_script("window.scrollBy(0,500);")
            time.sleep(0.1)
        products=driver.find_elements_by_xpath("//div[@class='css-12egk0t']/a[@class='css-ix8km1']") 
        products=[x.get_attribute('href') for x in products]   
        total_products.extend(products)
        
        try:
            time.sleep(0.5)
            driver.find_element_by_xpath("//*[name()='svg' and @class='css-15yx468 ']").click()
            #driver.find_element_by_xpath("//button[@class='css-812ha7 ']").click()
        except Exception as e:
            print(e)
            break   
    print(len(total_products))
    for p in total_products:
        driver.get(p)

        product_dic={}
        try:
            brand_name = driver.find_element_by_xpath("//h1/a/span[@class='css-15zphjk ']").text
        except:
            brand_name = ''
        try:
            product_name = driver.find_element_by_xpath("//h1/span[@class='css-r4ddnb ']").text
        except:
            product_name=''
        try:
            num_reviews = driver.find_element_by_xpath("//button/span[@class='css-rok4hb ']").text
        except:
            num_reviews=''
        try:
            price = driver.find_element_by_xpath("//div/div[@data-comp='Price Box']").text
        except:
            price=''
        try:
            love_count = driver.find_element_by_xpath("//span[@data-at='product_love_count']").text
        except:
            love_count=''
        try:
            category = driver.find_element_by_xpath("//button[@class='css-r6l5nz ']").text
        except:
            category = ''

        try:
            category_1=driver.find_element_by_xpath("//button[@class='css-r6l5nz ']").text
        except:
            category_1 = ''
        try:
            category_2=driver.find_element_by_xpath("//h1[@class='css-1cl2wdo ']").text
        except:
            category_2 = ''
        print(brand_name)
        print(num_reviews)
        print(price)
        print(details_info)
        print(love_count)
        print(category_1)
        print(category_2)

        rating = 'No Rating'
        for i in range(50):

            try:
                driver.execute_script("window.scrollBy(0, 80);")
                rating= driver.find_element_by_xpath("//div[@class='css-14yihrc ']/div[@class='css-ffj77u ']").text[0:3]
                print(rating)               
                break
            except:
                continue

 
        product_dic['brand_name']=brand_name
        product_dic['product_name']=product_name
        product_dic['num_reviews']=num_reviews
        product_dic['price']=price
        product_dic['love_count']=love_count
        product_dic['rating']=rating
        product_dic['category']=category
        product_dic['category_1']=category_1
        product_dic['category_2']=category_2
        
        product_list.append(product_dic)

keys = product_list[0].keys()
with open('sephora_noncrueltyfree.csv', 'w') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(product_list)

driver.close()
      


 