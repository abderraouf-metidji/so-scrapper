from bdd import get_database
from scrap_beautifulsoup import get_questions as get_questions_bs
from scrap_selenium import get_questions as get_questions_selenium, setup_driver
from multiprocessing.pool import ThreadPool

"""
Méthode pour scraper les données et les insérer dans la base de données
"""
def scrap_data():
    """
    On demande à l'utilisateur de choisir la méthode de scraping
    """
    method = input("Do you want to use Selenium or BeautifulSoup for scraping? (1/2): ").strip().lower()
    if method not in ["1", "2"]:
        print("Invalid choice. Please select '1' or '2'.")
        return
    
    number_of_pages = int(input("How many pages do you want to scrape? "))
    
    """
    On récupère les questions
    """
    if method == "selenium":
        driver = setup_driver()
        questions = get_questions_selenium(driver, number_of_pages)
        driver.quit()
    else:
        questions = get_questions_bs(number_of_pages)
        
    """"
    Boucle de multithreading pour scraper les questions en parallèle
    """
    if method == "2":
        with ThreadPool(10) as pool:
            questions_list = pool.map(get_questions_bs, range(1, number_of_pages + 1))
            pool.close()
    else:
        with ThreadPool(10) as pool:
            questions_list = pool.map(get_questions_selenium, range(1, number_of_pages + 1))
            pool.close()
            
    """
    Flatten the list of lists
    """
    questions = [question for sublist in questions_list for question in sublist]

    """
    On se connecte à la base de données
    """
    dbname = get_database()
    collection = dbname['questions']
    """
    On supprime les anciennes questions de la base de données
    """
    collection.delete_many({})
    """
    On insère les questions dans la base de données
    """
    collection.insert_many(questions)
    print(f"Inserted {len(questions)} questions into the database.")

if __name__ == "__main__":
    scrap_data()