import requests
from bs4 import BeautifulSoup

def fetch_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        print(f"Request failed with status code {response.status_code}")
        return None

def get_number_of_pages(soup):
    pages = soup.find_all('a', class_='s-pagination--item js-pagination-item')
    if pages:
        return int(pages[-2].text.strip())
    return 1

def get_questions_from_page(soup):
    questions = []
    for question in soup.find_all('div', class_='s-post-summary'):
        title = question.find('h3', class_='s-post-summary--content-title')
        title = title.text.strip() if title else None
        link = question.find('h3').find('a')
        link = "https://stackoverflow.com" + link['href'] if link else None
        summary = question.find('div', class_='s-post-summary--content-excerpt')
        summary = summary.text.strip() if summary else None
        tags = [tag.text for tag in question.find_all('a', class_='post-tag')] or None
        author_element = question.select_one('div.s-user-card__minimal div.s-user-card--info div.s-user-card--link a')
        author = author_element.text.strip() if author_element else None
        date = question.find('span', class_='relativetime')
        date = date['title'] if date else None
        questions.append({
            'title': title,
            'link': link,
            'summary': summary,
            'tags': tags,
            'author': author,
            'date': date
        })
    return questions

def get_questions_for_page(page_number):
    base_url = "https://stackoverflow.com/questions?tab=newest&page="
    page_url = base_url + str(page_number)
    page_content = fetch_page(page_url)
    if page_content:
        soup = BeautifulSoup(page_content, 'html.parser')
        return get_questions_from_page(soup)
    return []

def get_number_of_pages(soup):
    pages = soup.find_all('a', class_='s-pagination--item js-pagination-item')
    if pages:
        return int(pages[-2].text.strip())
    return 1
