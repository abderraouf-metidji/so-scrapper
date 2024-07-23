from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run headless Chrome
    service = ChromeService(executable_path='/path/to/chromedriver')  # Update path to your chromedriver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def fetch_page(driver, url):
    driver.get(url)
    # Wait for the page to load and for the questions to be visible
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 's-post-summary'))
    )
    return driver.page_source

def get_questions_from_page(driver):
    questions = []
    post_summaries = driver.find_elements(By.CLASS_NAME, 's-post-summary')
    for post_summary in post_summaries:
        title = post_summary.find_element(By.CLASS_NAME, 's-post-summary--content-title').text
        link_element = post_summary.find_element(By.TAG_NAME, 'a')
        link = "https://stackoverflow.com" + link_element.get_attribute('href')
        summary = post_summary.find_element(By.CLASS_NAME, 's-post-summary--content-excerpt').text
        tags = [tag.text for tag in post_summary.find_elements(By.CLASS_NAME, 'post-tag')]
        author_element = post_summary.find_element(By.CSS_SELECTOR, 'div.s-user-card__minimal div.s-user-card--info div.s-user-card--link a')
        author = author_element.text
        date = post_summary.find_element(By.CLASS_NAME, 'relativetime').get_attribute('title')
        questions.append({
            'title': title,
            'link': link,
            'summary': summary,
            'tags': tags,
            'author': author,
            'date': date
        })
    return questions

def get_number_of_pages(driver):
    base_url = "https://stackoverflow.com/questions?tab=newest&page=1"
    fetch_page(driver, base_url)  # Load the page to get the page count
    page_elements = driver.find_elements(By.CSS_SELECTOR, 'a.s-pagination--item')
    if page_elements:
        return int(page_elements[-2].text.strip())  # Get the second to last element which is the last page number
    return 1

def get_questions_for_page(driver, page_number):
    base_url = "https://stackoverflow.com/questions?tab=newest&page="
    page_url = base_url + str(page_number)
    fetch_page(driver, page_url)
    return get_questions_from_page(driver)
