# test_insertion_bdd.py
import pytest
import mongomock
from bdd import get_database

@pytest.fixture
def mock_db():
    # Use mongomock for testing
    db = mongomock.MongoClient().db
    return db

def test_database_insertion(mock_db):
    # Simulate the function that inserts data
    def insert_fake_data(db):
        collection = db['questions']
        fake_data = [
            {'title': 'Question 1', 'link': 'http://example.com/1', 'summary': 'Summary 1', 'tags': ['tag1'], 'author': 'Author 1', 'date': '2024-07-23'},
            {'title': 'Question 2', 'link': 'http://example.com/2', 'summary': 'Summary 2', 'tags': ['tag2'], 'author': 'Author 2', 'date': '2024-07-24'}
        ]
        collection.insert_many(fake_data)

    # Call the function to insert fake data
    insert_fake_data(mock_db)

    # Verify the data is inserted correctly
    collection = mock_db['questions']
    assert collection.count_documents({}) == 2
    data = list(collection.find())
    assert len(data) == 2
    assert data[0]['title'] == 'Question 1'
    assert data[1]['title'] == 'Question 2'
