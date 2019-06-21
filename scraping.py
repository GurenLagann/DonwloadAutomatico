import urllib.request
from bs4 import BeautifulSoup
import time
import pandas as pd
from selenium import webdriver
import Pabx

def Teste1 ():
    driver.get(urlpage)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    time.sleep(30)