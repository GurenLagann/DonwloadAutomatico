import urllib.request
from bs4 import BeautifulSoup
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = webdriver.ChromeOptions()
options.add_argument("download.default_directory=C:/Downloads")

driver = webdriver.Chrome(chrome_options=options)

# Iniciando o Navegador e encaminhando para o IP da Página
driver = webdriver.Chrome('chromedriver.exe')
driver.get("http://192.168.3.1/pbxip/framework/")

# Comandos em JavaScript para adicionar login e senha e acessar a página
jscomand = "document.nonautenticated2.submit();"
driver.execute_script(
    "document.getElementById('authusername').value = 'master'")
driver.execute_script(
    "document.getElementById('authpassword').value = 'Agil@agg9809GG'")
driver.execute_script(jscomand)

arq = '/var/spool/asterisk/monitor/20190515-1557958979.131891-1557958980.wav'
driver.get(
    'http://192.168.3.1/pbxip/core/includes/downloadaudioMp3.php?file=' + arq)
