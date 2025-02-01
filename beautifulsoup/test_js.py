from selenium import webdriver 
from bs4 import BeautifulSoup 
#from selenium.webdriver.common.by import By

# Set up the browser 
driver = webdriver.Chrome() 
#driver.get("https://dynamic-website.com")
driver.get("https://www.lutrija.hr/hl/rezultati/eurojackpot")
 
# Get the page source after the JavaScript has executed 
page_source = driver.page_source 
 
# Use BeautifulSoup to parse the HTML 
soup = BeautifulSoup(page_source, 'html.parser') 
 
# Scrape the desired data from the soup object 
# … 

#show-more-button-container
#showMoreButtonContainer = driver.find_element(By.CLASS_NAME,'show-more-button-container')
#showMoreButtonContainer.click()
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