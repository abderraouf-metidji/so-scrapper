import unittest
from unittest.mock import patch
from scrap_beautifulsoup import fetch_page


class TestFetchPage(unittest.TestCase):
    """
    Une classe de test pour tester la fonction fetch_page.
    """

    @patch('scrap_beautifulsoup.requests.get')
    def test_fetch_page_success(self, mock_get):
        """
        Teste la fonction fetch_page pour une requête réussie.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = b"Contenu de la page"
        
        url = "https://stackoverflow.com"
        result = fetch_page(url)
        
        self.assertEqual(result, b"Contenu de la page")

if __name__ == '__main__':
    unittest.main()
