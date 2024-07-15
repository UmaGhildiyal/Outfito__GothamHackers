from flask import Flask, render_template, request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    keywords = request.form['keywords']
    image_urls = search_pinterest(keywords)
    return render_template('index.html', image_urls=image_urls)

def search_pinterest(keywords):
    # Set up Selenium
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    # Specify the path to the ChromeDriver executable
    chromedriver_path = 'C:/Users/SUHANI SHARMA/OneDrive/Desktop/chromedriver-win64/chromedriver-win64/chromedriver.exe'  # Update this to the correct path
    service = ChromeService(executable_path=chromedriver_path)
    
    driver = webdriver.Chrome(service=service, options=options)

    try:
        query = "+".join(keywords.split())
        url = f"https://www.pinterest.com/search/pins/?q={query}"
        driver.get(url)
        time.sleep(3)  # Wait for the page to load

        # Scroll to load more images
        for _ in range(3):
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
            time.sleep(2)

        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        image_urls = []
        for img_tag in soup.find_all('img', {'src': True}):
            img_url = img_tag['src']
            if img_url.startswith('https://i.pinimg.com/') and '236x' in img_url:
                image_urls.append(img_url)
        
        return image_urls[:10]  # Limit to top 10 images
    finally:
        driver.quit()

if __name__ == '__main__':
    app.run(debug=True)

