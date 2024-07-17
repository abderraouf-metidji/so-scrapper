from bdd import get_database
from scrap_beautifulsoup import get_questions

"""Méthode pour scraper les données et les insérer dans la base de données"""
def scrap_data():
    number_of_pages = int(input("How many pages do you want to scrape? "))
    questions = get_questions(number_of_pages)
    """On se connecte à la base de données"""
    dbname = get_database()
    collection = dbname['questions']
    """On supprime les anciennes questions de la base de données"""
    collection.delete_many({})
    """On insère les questions dans la base de données"""
    collection.insert_many(questions)
    print(f"Inserted {len(questions)} questions into the database.")

if __name__ == "__main__":
    scrap_data()