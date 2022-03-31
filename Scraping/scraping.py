from selenium import webdriver
import os
import time
import urllib.request
import base64

def save_image(file_content, file_name):
    try:
       file_content=base64.b64decode(file_content)
       with open("C:\\Crawler\\temp\\" + file_name,"wb") as f:
            f.write(file_content)
    except Exception as e:
       print(str(e))

# Using Chrome to access web
driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriver"))


# Open the website
driver.get('https://www.google.com/search?q=person+holding+a+gun&tbm=isch&ved=2ahUKEwi2v4no_OP2AhUDZRoKHapeB-YQ2-cCegQIABAA&oq=person+holding+a+gun&gs_lcp=CgNpbWcQAzIHCCMQ7wMQJzIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDoECAAQQzoICAAQgAQQsQM6CwgAEIAEELEDEIMBOgUIABCxAzoKCCMQ7wMQ6gIQJ1CZBViTJGC2JWgGcAB4AIABpAGIAdkMkgEEMTguM5gBAKABAaoBC2d3cy13aXotaW1nsAEKwAEB&sclient=img&ei=gSE_Yvb6HoPKaaq9nbAO&bih=976&biw=1920')

time.sleep(3)

count = 0
driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
time.sleep(10)

# Find cam button
images = driver.find_elements_by_css_selector('.PNCib a img')

for img in images:
    try:
        time.sleep(1)
        img.click()
        time.sleep(3)

        # print('--------------------------------------------------')
        base64_image_data = driver.find_element_by_css_selector('img.n3VNCb').get_attribute('src').split(",")[1]
        data = base64.b64decode(base64_image_data)

        with open(f"gun/img{count + 1}.png", mode="wb") as f:
            f.write(data)

        urllib.request.urlretrieve(driver.find_element_by_css_selector('img.n3VNCb').get_attribute('src'), f"gun/img{count + 1}.png")


        count = count+1

    except Exception as e:
        print(e)