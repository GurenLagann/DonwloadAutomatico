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
driver.execute_script("document.getElementById('authusername').value = 'master'")
driver.execute_script("document.getElementById('authpassword').value = 'Agil@agg9809GG'")
driver.execute_script(jscomand)

# Comando para redirecionar a página indicada e alterar campos especificos
driver.get("http://192.168.3.1/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbG  xzLmRldGFpbGVk")
driver.execute_script("document.getElementById('calldate_day_start').value = '15/05/2019'")
driver.execute_script("document.getElementById('calldate_day_end').value = '15/05/2019'")

#button = driver.execute_script("document.getElementById('confirm')")
#button.click()

#Download Automátio 
arq = '/var/spool/asterisk/monitor/20190515-1557958979.131891-1557958980.wav'
driver.get('http://192.168.3.1/pbxip/core/includes/downloadaudioMp3.php?file=' + arq)
    

# proximos passos:
# aprender como iniciar o download e como alterar o nome do arquivo? 
# e como fazer isso para um conjunto de arquivos especificos? 
