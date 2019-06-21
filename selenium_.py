from selenium import webdriver
import selenium
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time

user = "master"
pwd = "Agil@agg9809GG"

driver = webdriver.Chrome('chromedriver.exe')
driver.get("http://192.168.3.1")
driver.execute_script("document.getElementById('authusername')").send_keys(user)
driver.execute_script("document.getElementById('authpassword')").send_keys(pwd
driver.execute_script("document.nonautenticated2.submit();")


    
