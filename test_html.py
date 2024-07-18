import unittest
import requests
from bs4 import BeautifulSoup
from scrap_beautifulsoup import get_number_of_pages

class TestNumberOfPages(unittest.TestCase):
    """
    Une classe de cas de test pour tester la fonctionnalité de la fonction get_number_of_pages.
    """

    def test_get_number_of_pages(self):
        url = "https://stackoverflow.com/questions?tab=newest"
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        
        soup = BeautifulSoup(response.content, 'html.parser')
        result = get_number_of_pages(soup)
        
        print(f"Nombre de pages trouvées : {result}")
        
        self.assertIsInstance(result, int)
        self.assertGreaterEqual(result, 1)

if __name__ == '__main__':
    unittest.main()
