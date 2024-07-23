import requests
import datetime

"""
Ce script permet de récupérer les 5 dernières questions posées sur StackOverflow
"""
url = "https://api.stackexchange.com/2.3/questions"
params = {
    'order': 'desc',
    'sort': 'activity',
    'site': 'stackoverflow',
    'filter': 'withbody',
    'pagesize': 5
}

"""
Le code suivant permet de récupérer les données de l'API StackOverflow
"""
response = requests.get(url, params=params)
data = response.json()

"""
Le code suivant permet d'afficher les données récupérées
"""
print("5 dernières questions posées sur StackOverflow :")
for question in data['items']:
    question_id = question['question_id']
    title = question['title']
    link = f"https://stackoverflow.com/q/{question_id}"
    summary = question.get('body', 'No summary available')
    tags = question.get('tags', [])
    author_id = question['owner']['user_id']
    author_name = question['owner']['display_name']
    creation_date = question['creation_date']
    
    creation_date = datetime.datetime.fromtimestamp(creation_date).strftime('%Y-%m-%d %H:%M:%S')

    """
    Le code suivant permet d'afficher les données de chaque question
    """
    print(f"Question ID: {question_id}")
    print(f"Title: {title}")
    print(f"Link: {link}")
    print(f"Summary: {summary}")
    print(f"Tags: {', '.join(tags)}")
    print(f"Author: {author_name} (User ID: {author_id})")
    print(f"Published on: {creation_date}")
    print()
