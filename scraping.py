# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():

    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    # save return variables
    news_title, news_paragraph = mars_news(browser)

    data = {
        'news_title': news_title,
        'news_paragraph': news_paragraph,
        'featured_image': featured_image(browser),
        'facts': mars_facts(),
        'hemispheres': hemi_scrape(browser),
        'last_modified': dt.datetime.now()
    }

    # Close the automated browser
    browser.quit()
    
    return data

def mars_news(browser):

    # Visit the Mars NASA news site
    url = 'https://redplanetscience.com'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)


    # Use BS4 to identify elements to scrape
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        slide_elem.find('div', class_='content_title')
        news_title = slide_elem.find('div', class_='content_title').get_text()
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    except AttributeError:
        return None, None
    
    return news_title, news_p

def featured_image(browser):

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

    # Error handling
    try:
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    except AttributeError:
        return None

    # Create full link URL
    img_url = f'{url + img_url_rel}'

    return img_url

def mars_facts():

    # Visit new page
    url = 'https://galaxyfacts-mars.com/'

    # Error handling
    try:
        # Pull in Earth to Mars comparison table. Line commented-out below is optional but provides a more concise df
        df = pd.read_html(url)[0]
    except BaseException:
        return None

    df.columns = ['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)
    # df = df.iloc[1:,:]

    # Convert df to html
    return df.to_html()

def hemi_scrape(browser):

    # Use browser to visit the URL 
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    browser.is_element_present_by_css('div.wrapper', wait_time=1)

    # Write code to retrieve the image urls and titles for each hemisphere.
    hemisphere_image_urls = []
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

    browser.quit()

    return hemisphere_image_urls

if __name__ == '__main__':
    print(scrape_all())