from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bdd import get_database
import logging

def setup_driver():
    """
    Configure le driver Selenium pour le navigateur Chrome.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Exécuter Chrome en mode headless
    chrome_options.add_argument("--log-level=3")  # Réduire le niveau des logs
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])  # Ignorer les logs de Chrome
    service = ChromeService()
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def ignore_selenium_log():
    """
    Ignore les messages de log spécifiques à Selenium.
    """
    logging.getLogger('urllib3.connectionpool').setLevel(logging.ERROR)

def fetch_page(driver, url):
    """
    Charge la page web à partir de l'URL donnée.
    """
    driver.get(url)
    return driver.page_source

def get_questions_from_page(driver):
    """
    Extrait les questions d'une page web chargée par Selenium.
    """
    questions = []
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 's-post-summary')))
        post_summaries = driver.find_elements(By.CLASS_NAME, 's-post-summary')
        for post_summary in post_summaries:
            try:
                title = post_summary.find_element(By.CLASS_NAME, 's-post-summary--content-title').text
                link_element = post_summary.find_element(By.TAG_NAME, 'a')
                link = link_element.get_attribute('href')
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
            except Exception as e:
                logging.error(f"Erreur lors du traitement de la question : {e}")
    except Exception as e:
        logging.error(f"Erreur lors de l'attente des résumés de questions : {e}")
    return questions

def get_questions_for_page(page_number):
    """
    Récupère les questions pour un numéro de page donné.
    """
    base_url = "https://stackoverflow.com/questions?tab=newest&page="
    page_url = base_url + str(page_number)
    driver = setup_driver()
    fetch_page(driver, page_url)
    questions = get_questions_from_page(driver)
    driver.quit()
    return questions

def scrape_page(page_number):
    """
    Fonction de scraping pour une page donnée, utilisée pour la gestion des threads.
    """
    return get_questions_for_page(page_number)
