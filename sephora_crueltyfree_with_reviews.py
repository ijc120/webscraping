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
review_list = []
brands = ['https://www.sephora.com/brand/tarte','https://www.sephora.com/brand/josie-maran','https://www.sephora.com/brand/beautyblender','https://www.sephora.com/brand/becca-cosmetics','https://www.sephora.com/brand/bite-beauty','https://www.sephora.com/brand/captain-blankenship','https://www.sephora.com/brand/christophe-robin','https://www.sephora.com/brand/ciate','https://www.sephora.com/brand/commodity','https://www.sephora.com/brand/coola-suncare','https://www.sephora.com/brand/cover-fx','https://www.sephora.com/brand/deborah-lippmann','https://www.sephora.com/brand/drybar','https://www.sephora.com/brand/dr-dennis-gross-skincare','https://www.sephora.com/brand/first-aid-beauty','https://www.sephora.com/brand/gloss-moderne','https://www.sephora.com/brand/hourglass','https://www.sephora.com/brand/herbivore-botanicals','https://www.sephora.com/brand/ilia','https://www.sephora.com/brand/it-cosmetics','https://www.sephora.com/brand/jack-black','https://www.sephora.com/brand/kate-somerville','https://www.sephora.com/brand/kora-organics','https://www.sephora.com/brand/milk-makeup','https://www.sephora.com/brand/murad','https://www.sephora.com/brand/natasha-denona','https://www.sephora.com/brand/ole-henriksen','https://www.sephora.com/brand/omorovicza','https://www.sephora.com/brand/ouai-haircare','https://www.sephora.com/brand/rahua','https://www.sephora.com/brand/ren','https://www.sephora.com/brand/smashbox','https://www.sephora.com/brand/sunday-riley','https://www.sephora.com/brand/supergoop','https://www.sephora.com/brand/tatcha','https://www.sephora.com/brand/too-faced','https://www.sephora.com/brand/vernon-francois','https://www.sephora.com/brand/wander-beauty']


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
        except Exception as e:
            print(e)
            break   
    print(len(total_products))

    for p in products:
        driver.get(p)
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
        
        rating = 'No Rating'
        for i in range(50):
            try:
                driver.execute_script("window.scrollBy(0, 80);")
                rating= driver.find_element_by_xpath("//div[@class='css-14yihrc ']/div[@class='css-ffj77u ']").text[0:3]
                break
            except:
                continue
        j = 1
        while True:
            try:
                click_button= driver.find_element_by_xpath("//button[@class='css-2wz498 ']").click()
                j+=1
            if j==10:
                break
            else:
                continue
            except:
                break

        reviews= driver.find_elements_by_xpath("//div[@data-comp='Review']") 
        print(len(reviews))

        for r in reviews:
            review={}

            text = r.find_element_by_xpath(".//div[@data-comp='Ellipsis Box']").text
            date = r.find_element_by_xpath(".//span[@class='css-12z5fyi ']").text
            try:
                title = r.find_element_by_xpath(".//div[@class='css-1fsuw0x ']").text
            except:
                title = ''  
            
            review['brand_name']=brand_name
            review['text']= text
            review['date']=date
            review['title']=title
            review['category']=category
            review['product_name']=product_name
            review['num_reviews']=num_reviews
            review['price']=price
            review['details_info']=details_info
            review['love_count']=love_count
            review['rating']=rating

            review_list.append(review)
            
            
keys = review_list[0].keys()
with open('sephora.csv', 'w') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(review_list)

driver.close()