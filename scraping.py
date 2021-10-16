def scrape_all():
    # Import Splinter and BeautifulSoup
    from splinter import Browser
    from bs4 import BeautifulSoup as soup
    from webdriver_manager.chrome import ChromeDriverManager
    import pandas as pd

    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Visit the Mars NASA news site
    url = 'https://redplanetscience.com'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)


    # Use BS4 to identify elements to scrape
    html = browser.html
    news_soup = soup(html, 'html.parser')
    slide_elem = news_soup.select_one('div.list_text')
    slide_elem.find('div', class_='content_title')
    news_title = slide_elem.find('div', class_='content_title').get_text()
    news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

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

    # Create full link URL
    img_url = f'{url + img_url_rel}'

    # Visit new page
    url = 'https://galaxyfacts-mars.com/'
    browser.visit(url)
    browser.is_element_present_by_css('div.container-fluid', wait_time=1)
    html = browser.html
    fact_soup = soup(html, 'html.parser')

    # Pull in Earth to Mars comparison table. Line 54 is optional but creates a more concise df
    df = pd.read_html(url)[0]
    df.columns = ['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)
    # df = df.iloc[1:,:]

    # Convert df to html
    df.to_html()

    # Close the automated browser
    browser.quit()