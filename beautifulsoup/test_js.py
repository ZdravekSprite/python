from selenium import webdriver 
from bs4 import BeautifulSoup 
import time
from selenium.webdriver.common.by import By

url = "https://www.lutrija.hr/hl/rezultati/eurojackpot"

# Set up the browser 
options = webdriver.ChromeOptions()
#options.add_argument('--headless')
#driver = webdriver.Chrome(options=options)
driver = webdriver.Chrome()
#driver = webdriver.Firefox()

# Navigate to URL
driver.get(url)
time.sleep(5)

while True:
    # Click
    btn_elements = driver.find_elements(By.CLASS_NAME, "btn-default")
    if len(btn_elements):
        #btn_element.click()
        driver.execute_script("arguments[0].click()", btn_elements[0])
        time.sleep(5)
    else:
        break

# Get the page source after the JavaScript has executed 
page_source = driver.page_source 
 
# Use BeautifulSoup to parse the HTML 
soup = BeautifulSoup(page_source, 'html.parser') 
 
kola = []
for div in soup.find_all('div', class_='result-numbers'):
    kolo = []
    drawDateTime_div = div.find('div', class_='drawDateTime')
    kolo_div = drawDateTime_div.find('div')
    print(kolo_div.text)
    kolo.append(kolo_div.text)
    dateTime_span = drawDateTime_div.find('span', class_='date-time')
    dt_txt = dateTime_span.text
    #print(dt_txt.replace(''))
    kolo.append(dt_txt.replace(' \n ',' '))
    winningNumbers_div = div.find('div', class_='winning-numbers')
    eurojackpot_div = div.find('div', class_='EUROJACKPOT')
    lis = div.find_all('li')
    for li in lis:
        #print(li.text)
        kolo.append(li.text)
    #print(div.text)
    kola.append(kolo)

# Close the browser 
driver.quit()

for k in kola:
    print('kolo',k)