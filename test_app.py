import pytest
import app as library


@pytest.fixture
def client():
    library.app.config["TESTING"] = True
    return library.app.test_client()


def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Library Management System" in response.data


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_api_books(client):
    response = client.get("/api/books")
    assert response.status_code == 200
    assert len(response.get_json()["books"]) >= 1


def test_search(client):
    response = client.get("/?q=clean")
    assert b"Clean Code" in response.data
    assert b"The Alchemist" not in response.data


def test_add_book(client):
    before = len(library.BOOKS)
    client.post("/add", data={"title": "Test Book", "author": "Test Author"})
    assert len(library.BOOKS) == before + 1


def test_issue_and_return(client):
    client.post("/add", data={"title": "Flow Book", "author": "Someone"})
    book_id = library.BOOKS[-1]["id"]
    client.post(f"/issue/{book_id}")
    assert library.find_book(book_id)["status"] == "Issued"
    client.post(f"/return/{book_id}")
    assert library.find_book(book_id)["status"] == "Available"
