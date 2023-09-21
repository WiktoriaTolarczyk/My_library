from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import time
#set chromodriver.exe path
driver = webdriver.Firefox()
driver.implicitly_wait(0.5)
#launch URL
driver.get("https://www.empik.com//")
#identify search box
m = driver.find_element(By.CLASS_NAME, 'css-18n58r')
#enter search text
#perform Google search with Keys.ENTER
time.sleep(0.3)
ActionChains(driver) \
    .click(m) \
    .perform()
m = driver.find_element(By.CLASS_NAME, 'css-1rwl265-input-1')
time.sleep(0.3)
m.send_keys("Miasto jadeitu")
time.sleep(0.3)
m.send_keys(Keys.ENTER)
time.sleep(0.3)
# m = driver.find_element(By.CLASS_NAME, 'DesktopPriceStyles')
# print(m)
# m.send_keys("Tutorialspoint")
# time.sleep(0.2)
# #perform Google search with Keys.ENTER
# m.send_keys(Keys.ENTER)