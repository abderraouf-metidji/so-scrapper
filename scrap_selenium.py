import logging
from selenium.webdriver.remote.remote_connection import LOGGER
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

"""
On désactive les logs de Selenium
"""

LOGGER.setLevel(logging.WARNING)

"""
Setup the Selenium WebDriver
"""

def setup_driver():
    options = Options()
    options.add_argument('--headless')  # Run in headless mode
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

"""
Méthode pour vérifier si la requête a réussi ou non
"""

def fetch_page(driver, url):
    driver.get(url)
    return driver.page_source

"""
Méthode pour récupérer le nombre de pages à scraper
"""

def get_number_of_pages(driver):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    pages = soup.find_all('a', class_='s-pagination--item')
    if pages:
        return int(pages[-2].text.strip())
    return 1

"""
Méthode pour récupérer les questions de la page ainsi que les autres données nécessaires
"""

def get_questions_from_page(soup):
    questions = []
    """
    Ici on va identifier l'emplacement des question dans le code html de la page
    """

    for question in soup.find_all('div', class_='s-post-summary'):
        """
        On récupère tout d'abord le titre de la question
        """

        title = question.find('h3', class_='s-post-summary--content-title')
        title = title.text.strip() if title else None
        """
        On récupère le lien de la question
        """

        link = question.find('h3').find('a')
        link = "https://stackoverflow.com" + link['href'] if link else None
        """
        On récupère le résumé de la question
        """

        summary = question.find('div', class_='s-post-summary--content-excerpt')
        summary = summary.text.strip() if summary else None
        """
        On récupère les tags de la question
        """

        tags = [tag.text for tag in question.find_all('a', class_='post-tag')] or None
        """
        On récupère l'auteur de la question
        """

        author_element = question.select_one('div.s-user-card__minimal div.s-user-card--info div.s-user-card--link a')
        author = author_element.text.strip() if author_element else None
        """
        On récupère la date de la question
        """

        date = question.find('span', class_='relativetime')
        date = date['title'] if date else None
        """
        On ajoute les données récupérées dans un dictionnaire au format json
        """

        questions.append({
            'title': title,
            'link': link,
            'summary': summary,
            'tags': tags,
            'author': author,
            'date': date
        })
    return questions

"""
Méthode pour récupérer les questions de toutes les pages
"""

def get_questions(driver, number_of_pages):
    base_url = "https://stackoverflow.com/questions?tab=newest&page="
    all_questions = []

    for page in range(1, number_of_pages + 1):
        print(f"Scraping page {page}...")
        page_url = base_url + str(page)
        page_content = fetch_page(driver, page_url)
        soup = BeautifulSoup(page_content, 'html.parser')
        questions = get_questions_from_page(soup)
        all_questions.extend(questions)
    
    return all_questions
