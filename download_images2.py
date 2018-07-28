import requests
import urllib.request
from bs4 import BeautifulSoup

site = 'https://weheartit.com'

def get_image(url, file_path, filename):
    full_path = file_path + filename + '.jpeg'
    urllib.request.urlretrieve(url,full_path)


response = requests.get(site)

soup = BeautifulSoup(response.text, 'html.parser')
img_tags = soup.find_all('img')
urls = [img['src'] for img in img_tags]


counter = 0
for url in urls:
    counter = counter + 1
    filename = "{}{}".format('result_image',counter)
    get_image(url, 'result_folder/', filename)



