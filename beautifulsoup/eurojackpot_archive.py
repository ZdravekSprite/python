import os
import csv
from FileManager import *

#pip install bs4
from bs4 import BeautifulSoup 
#pip install selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.sep.join([SCRIPT_DIR, 'EUROJACKPOT_old.csv'])

def get_kola(url, kola):
    # Set up the browser 
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    #driver = webdriver.Chrome()
    #driver = webdriver.Firefox()

    # Navigate to URL
    driver.get(url)
    time.sleep(5)

    # Get the page source after the JavaScript has executed 
    page_source = driver.page_source 
    
    # Use BeautifulSoup to parse the HTML 
    soup = BeautifulSoup(page_source, 'html.parser') 

    for tr in soup.find_all('tr'):
        kolo = []
        tds = tr.find_all('td')
        if tds:
            kolo.append(tds[0].text.strip())
            lis = tds[1].find_all('li')
            for li in lis:
                #print(li.text)
                kolo.append(li.text)
            kola.append(kolo)
            #kola.append(tr.text)

    # Close the browser 
    driver.quit()

kola = []

for godina in range(2012,2026):
    url = f"https://www.euro-jackpot.net/results-archive-{godina}"
    get_kola(url, kola)

#for k in kola:
#    print(k)
print(len(kola))

# writing to csv file
with open(CSV_FILE, 'w', encoding="windows 1252") as csvfile:
    # creating a csv writer object
    csvwriter = csv.writer(csvfile, delimiter=";",lineterminator='\n')
    # writing the fields
    #csvwriter.writerow(fields)
    # writing the data rows
    csvwriter.writerows(kola)