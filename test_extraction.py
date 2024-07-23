import unittest
import requests
from bs4 import BeautifulSoup
from scrap_beautifulsoup import get_questions_from_page

class TestQuestionExtraction(unittest.TestCase):
    """
    Une classe de cas de test pour tester l'extraction des questions à partir d'une page web.
    """

    def test_get_questions_from_page(self):
        url = "https://stackoverflow.com/questions?tab=newest"
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        
        soup = BeautifulSoup(response.content, 'html.parser')
        result = get_questions_from_page(soup)
        
        print(f"Données extraites : {result}")
        
        self.assertGreater(len(result), 0)
        
        for question in result:
            self.assertIn('title', question)
            self.assertIn('link', question)
            self.assertIn('summary', question)
            self.assertIn('tags', question)
            self.assertIn('author', question)
            self.assertIn('date', question)
            
            self.assertIsNotNone(question['title'])
            self.assertIsNotNone(question['link'])
            self.assertIsNotNone(question['summary'])
            self.assertIsNotNone(question['tags'])
            self.assertIsNotNone(question['author'])
            self.assertIsNotNone(question['date'])

if __name__ == '__main__':
    unittest.main()