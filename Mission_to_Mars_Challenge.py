# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# Set up Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=True)

# Visit the Mars NASA news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delat for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')
slide_elem

slide_elem.find('div', class_='content_title')

news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p

# Visit new page
url = 'https://spaceimages-mars.com/'
browser.visit(url)
browser.is_element_present_by_css('div.floating_text_area', wait_time=1)

# Click the button to display the full image
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Use BS4 to pull the link to the currently featured image
html = browser.html
img_soup = soup(html, 'html.parser')
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# Create full link URL
img_url = f'{url + img_url_rel}'
img_url

# Visit new page
url = 'https://galaxyfacts-mars.com/'
browser.visit(url)
browser.is_element_present_by_css('div.container-fluid', wait_time=1)
html = browser.html
fact_soup = soup(html, 'html.parser')

# Pull in Earth to Mars comparison table.
df = pd.read_html(url)[0]
df.columns = ['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df.to_html()
browser.quit()

# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'
browser = Browser('chrome', **executable_path, headless=False)
browser.visit(url)
browser.is_element_present_by_css('div.wrapper', wait_time=1)

# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
html = browser.html
img_soup = soup(html, 'html.parser')
items = img_soup.find_all('div', class_='item')

for item in items:
    hemispheres = {}
    link = item.find('a').get('href')
    browser.visit(url + link)
    link_html = browser.html
    link_soup = soup(link_html, 'html.parser')
    hemispheres['img_url'] = url + link_soup.find('a', text='Sample').get('href')
    hemispheres['title'] = link_soup.find('h2', class_='title').text
    hemisphere_image_urls.append(hemispheres)
    browser.back()

# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls

# 5. Quit the browser
browser.quit()