import requests
from bs4 import BeautifulSoup

url = "https://stackoverflow.com/questions"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

questions = []

for question in soup.find_all('div', class_='s-post-summary'):
    title = question.find('h3', class_='s-post-summary--content-title').text.strip()
    link = "https://stackoverflow.com" + question.find('h3').find('a')['href']
    summary = question.find('div', class_='s-post-summary--content-excerpt').text.strip()
    tags = [tag.text for tag in question.find_all('a', class_='post-tag')]
    author = question.find('div', class_='s-user-card').find('a').text.strip()
    date = question.find('span', class_='relativetime')['title']

    questions.append({
        'title': title,
        'link': link,
        'summary': summary,
        'tags': tags,
        'author': author,
        'date': date
    })

for q in questions:
    print(f"Title: {q['title']}")
    print(f"Link: {q['link']}")
    print(f"Summary: {q['summary']}")
    print(f"Tags: {', '.join(q['tags'])}")
    print(f"Author: {q['author']}")
    print(f"Date: {q['date']}")
    print("---")