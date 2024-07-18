import requests
from bs4 import BeautifulSoup

"""
Méthode pour récupérer le contenu de la page
"""
def fetch_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        print(f"Request failed with status code {response.status_code}")
        return None

"""
Méthode pour récupérer le nombre de pages à scraper
"""
def get_number_of_pages(soup):
    pages = soup.find_all('a', class_='s-pagination--item js-pagination-item')
    if pages:
        return int(pages[-2].text.strip())
    return 1

"""
Méthode pour récupérer les questions de la page ainsi que les autres données nécessaires
"""
def get_questions_from_page(soup):
    questions = []
    for question in soup.find_all('div', class_='s-post-summary'):
        title = question.find('h3', class_='s-post-summary--content-title')
        title = title.text.strip() if title else None
        """
        On récupère le lien de la question"""
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
def get_questions(number_of_pages):
    base_url = "https://stackoverflow.com/questions?tab=newest&page="
    all_questions = []
    """
    On boucle sur toutes les pages pour récupérer les questions
    """
    for page in range(1, number_of_pages + 1):
        print(f"Scraping page {page}...")
        page_url = base_url + str(page)
        page_content = fetch_page(page_url)
        if page_content:
            soup = BeautifulSoup(page_content, 'html.parser')
            questions = get_questions_from_page(soup)
            all_questions.extend(questions)
    
    return all_questions

"""
Méthode principale pour lancer le script
"""
if __name__ == "__main__":
    url = "https://stackoverflow.com/questions?tab=newest"
    page_content = fetch_page(url)
    if page_content:
        soup = BeautifulSoup(page_content, 'html.parser')
        number_of_pages = get_number_of_pages(soup)
        all_questions = get_questions(number_of_pages)
        for question in all_questions:
            print(question)
