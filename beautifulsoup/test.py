from bs4 import BeautifulSoup
#import bs4 as bs
import urllib.request

source = urllib.request.urlopen('https://www.ecb.europa.eu/euro/coins/2euro/html/index.en.html').read()

soup = BeautifulSoup(source, 'html.parser')

'''
# title of the page
print(soup.title)

# get attributes:
print(soup.title.name)

# get values:
print(soup.title.string)

# beginning navigation:
print(soup.title.parent.name)

# getting specific values:
print(soup.p)

for paragraph in soup.find_all('p'):
    print(paragraph.string)
    print(str(paragraph.text))

for div in soup.find_all('div', class_='body'):
    print(div.text)

inParsed = urllib.parse.urlparse(imagesname) # break down url
rootUrl = f'{inParsed.scheme}://{inParsed.netloc}' # to get root


imageUrl = urllib.parse.urljoin(rootUrl, imageUrl.get('src')) # add root to src
saveImgAs = [u for u in imageUrl.split('/') if u][-1] # get name from link

with open(saveImgAs, "wb") as f:
    f.write(requests.get(imageUrl).content) # download
    f.close()

print(saveImgAs, image)
'''
for div in soup.find_all('div', class_='box'):
    coins_div = div.find('div', class_='coins')
    images = coins_div.find_all('img')
    for image in images:
        # Print image source
        #print(image['src'])
        # Print alternate text
        #print(image['alt'])
        imageUrl = 'https://www.ecb.europa.eu'+image['src']
        saveImgAs = [u for u in imageUrl.split('/') if u][-2:]
        print(saveImgAs, imageUrl)
    content_div = div.find('div', class_='content-box')
    #print(content_div.text)
