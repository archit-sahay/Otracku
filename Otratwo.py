
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions

url="https://anilist.co/search/anime?search=zom%20100"
chrome_driver_path="C:\Program Files (x86)\chromedriver.exe"

options=webdriver.ChromeOptions()
# options.add_argument('headless')
# options.add_argument('window-size=1920x1080')
# options.add_argument("disable-gpu")
service=Service(executable_path=chrome_driver_path)
driver=webdriver.Chrome(service=service)#,options=options)
driver.get(url)
but=driver.find_elements(By.XPATH, '//*[@id="app"]/div[3]/div/div/div[4]/div[2]/div[2]/div[2]')
but[0].click()
# today=driver.find_elements(By.ID, "active-day")
# lol=driver.find_elements(By.CSS_SELECTOR, "a .show-title-bar")
anime=driver.find_elements(By.CLASS_NAME, "description")
name=driver.find_elements(By.CLASS_NAME, "title")
# time=today[0].find_elements(By.CSS_SELECTOR, "h3 .show-air-time")
ts=[]
all=[]

for ded in anime:
	all.append(str(ded.text))
for x in name:
	ts.append(str(x.text))
# for x in range(len(time)):
#     if anime[x].text != "":
#         ts[anime[x].text]=time[x].text
print(all)
print(x)
driver.quit()
