import pytest
import requests
from bs4 import BeautifulSoup
from scrap_beautifulsoup import get_number_of_pages

def test_get_number_of_pages():
    url = "https://stackoverflow.com/questions?tab=newest"
    response = requests.get(url)
    assert response.status_code == 200
    
    soup = BeautifulSoup(response.content, 'html.parser')
    result = get_number_of_pages(soup)
    
    print(f"Nombre de pages trouvées : {result}")
    
    assert isinstance(result, int)
    assert result >= 1

if __name__ == '__main__':
    pytest.main()
