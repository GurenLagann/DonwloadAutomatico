import urllib.request
from bs4 import BeautifulSoup
import time
import pandas as pd
from selenium import webdriver
import requests


def Teste1 ():
    req = requests.get(
        'http://192.168.3.1/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbG%20%20xzLmRldGFpbGVk')
    
    if req.status_code == 200:
        print('Requisição bem sucedida!')
        content = req.content

    soup = BeautifulSoup(content, 'html.parser')
    table = soup.find(name='table')

    table_str = str(table)
    rhtml = pd.read_html(table_str)[0]
    print(rhtml)