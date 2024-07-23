from concurrent.futures import ThreadPoolExecutor, as_completed
from bdd import get_database

def main():
    """
    Fonction principale qui demande à l'utilisateur de choisir la méthode de scraping
    (BeautifulSoup ou Selenium), et exécute la fonction de scraping correspondante.
    """
    print("Choisissez la méthode de scraping :")
    print("1: BeautifulSoup")
    print("2: Selenium")

    method = input("Entrez votre choix (1 ou 2) : ").strip()

    if method == "1":
        from scrap_beautifulsoup import scrape_page as scrape_page_bs
        scrape_pages(scrape_page_bs)
    elif method == "2":
        from scrap_selenium import scrape_page as scrape_page_selenium, ignore_selenium_log
        ignore_selenium_log()
        scrape_pages(scrape_page_selenium)
    else:
        print("Choix invalide. Veuillez sélectionner '1' ou '2'.")

def scrape_pages(scrape_page, number_of_pages=1, max_workers=4):
    """
    Exécute le scraping des pages spécifiées en utilisant des threads, 
    puis insère les questions récupérées dans la base de données.
    """
    number_of_pages = int(input("Combien de pages voulez-vous scraper ? "))
    pages = range(1, number_of_pages + 1)

    questions = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_page = {
            executor.submit(scrape_page, page): page
            for page in pages
        }

        for future in as_completed(future_to_page):
            page = future_to_page[future]
            try:
                page_questions = future.result()
                questions.extend(page_questions)
            except Exception as exc:
                print(f"La page {page} a généré une exception : {exc}")

    dbname = get_database()
    collection = dbname['questions']
    collection.delete_many({})
    collection.insert_many(questions)
    print(f"{len(questions)} questions insérées dans la base de données.")

if __name__ == "__main__":
    main()