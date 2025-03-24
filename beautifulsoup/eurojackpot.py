import os
#pip install bs4
from bs4 import BeautifulSoup 
#pip install selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
# importing csv module
import time
import datetime
import csv

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.sep.join([SCRIPT_DIR, 'EUROJACKPOT.csv'])

url = "https://www.lutrija.hr/hl/rezultati/eurojackpot"
kola = []

# csv file name
filename = CSV_FILE

# reading csv file
with open(filename, 'r', encoding="windows 1252") as csvfile:
    # creating a csv reader object
    csvreader = csv.reader(csvfile, delimiter=";")

    # extracting each data row one by one
    for row in csvreader:
        kola.append(row)

# Set up the browser 
options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
#driver = webdriver.Chrome()
#driver = webdriver.Firefox()

# Navigate to URL
driver.get(url)
time.sleep(5)

"""
while True:
    # Click
    btn_elements = driver.find_elements(By.CLASS_NAME, "btn-default")
    if len(btn_elements):
        #btn_element.click()
        driver.execute_script("arguments[0].click()", btn_elements[0])
        time.sleep(5)
    else:
        break
"""

# Get the page source after the JavaScript has executed 
page_source = driver.page_source 
 
# Use BeautifulSoup to parse the HTML 
soup = BeautifulSoup(page_source, 'html.parser') 

nova_kola = []

for div in soup.find_all('div', class_='result-numbers'):
    kolo = []
    drawDateTime_div = div.find('div', class_='drawDateTime')
    kolo_div = drawDateTime_div.find('div')
    print(kolo_div.text)
    kolo.append(kolo_div.text.split(" ")[1])
    dateTime_span = drawDateTime_div.find('span', class_='date-time')
    dt_txt = dateTime_span.text.replace(' \n ',' ').split(",")[1].strip()
    #print(dt_txt.replace(''))
    kolo.append(datetime.datetime.strptime(dt_txt, '%d.%m.%Y %H:%M'))
    winningNumbers_div = div.find('div', class_='winning-numbers')
    eurojackpot_div = div.find('div', class_='EUROJACKPOT')
    lis = div.find_all('li')
    for li in lis:
        #print(li.text)
        kolo.append(li.text)
    #print(div.text)
    if str(kolo[1]) != kola[0][1]:
        nova_kola.append(kolo)
    else:
        break

# Close the browser 
driver.quit()

for k in nova_kola:
    print('kolo',k)

nova_kola = nova_kola+kola

# writing to csv file
with open(filename, 'w', encoding="windows 1252") as csvfile:
    # creating a csv writer object
    csvwriter = csv.writer(csvfile, delimiter=";",lineterminator='\n')
    # writing the fields
    #csvwriter.writerow(fields)
    # writing the data rows
    csvwriter.writerows(nova_kola)