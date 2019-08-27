import re
import requests
import urllib.request as ur
from bs4 import BeautifulSoup as bs
from selenium import webdriver as wd

# Sd = str(input('Start Day: '))
# Ed = str(input('End Day: '))

Sda ="22/08/2019"
Eda ="22/08/2019"

link = 'http://192.168.3.1/pbxip/framework/container.ajax.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk%7CINCLUDE/aW5kZXgucmVwb3J0LnBocA'
link2 = ':http://192.168.3.1/pbxip/framework/container.ajax.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LnBocA..&where=0;start_filter|yes;calldate_day_start|22/08/2019;calldate_day_end|22/08/2019;calldate_time_start|00:00:00;calldate_time_end|23:59:59;src|;dst|;dcontext|;disposition|;disposition_colorize|1;disposition_icons|1;disposition_general|0;disposition_monitor|0;trunk|;branchname|;route|;var1|MQ..;var2|YWxs;var3|;var4|YToyOntzOjk6IklOU0VTU0lPTiI7czoxMDoicDJiX3BhaW5lbCI7czoxMzoiVVNFUl9VU0VSTkFNRSI7czo4OiJiV0Z6ZEdWeSI7fQ..&order=calldate&by=desc&page=1&limit=100&_=1566828895729'

# driver = wd.Chrome('./Webdriver/chromedriver')
# driver.get("http://192.168.3.1/pbxip/framework/")

#comandos para logar no site com comandos JavaScript
# driver.execute_script("document.getElementById('authusername').value = 'master'")
# driver.execute_script("document.getElementById('authpassword').value = 'Agil@agg9809GG'")
# driver.execute_script("document.nonautenticated2.submit();")
# driver.get(link2)


resp = requests.post(link, auth=("master","Agil@agg9809GG")) 
response = requests.get(link)

soup = bs(resp.text, 'html.parser')
print(soup)

for cookie in response.cookies:
    print(cookie.name, cookie.value)


