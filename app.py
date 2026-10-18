from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory data store (resets when the app restarts)
BOOKS = [
    {"id": 1, "title": "The Alchemist", "author": "Paulo Coelho", "status": "Available"},
    {"id": 2, "title": "Wings of Fire", "author": "A.P.J. Abdul Kalam", "status": "Issued"},
    {"id": 3, "title": "Clean Code", "author": "Robert C. Martin", "status": "Available"},
    {"id": 4, "title": "The Pragmatic Programmer", "author": "Andrew Hunt", "status": "Available"},
]


def find_book(book_id):
    return next((b for b in BOOKS if b["id"] == book_id), None)


@app.route("/")
def home():
    query = request.args.get("q", "").strip().lower()
    books = BOOKS
    if query:
        books = [b for b in BOOKS
                 if query in b["title"].lower() or query in b["author"].lower()]
    stats = {
        "total": len(BOOKS),
        "available": sum(1 for b in BOOKS if b["status"] == "Available"),
        "issued": sum(1 for b in BOOKS if b["status"] == "Issued"),
    }
    return render_template("index.html", books=books, stats=stats, query=query)


@app.route("/add", methods=["POST"])
def add_book():
    title = request.form.get("title", "").strip()
    author = request.form.get("author", "").strip()
    if title and author:
        new_id = max((b["id"] for b in BOOKS), default=0) + 1
        BOOKS.append({"id": new_id, "title": title, "author": author, "status": "Available"})
    return redirect(url_for("home"))


@app.route("/issue/<int:book_id>", methods=["POST"])
def issue_book(book_id):
    book = find_book(book_id)
    if book and book["status"] == "Available":
        book["status"] = "Issued"
    return redirect(url_for("home"))


@app.route("/return/<int:book_id>", methods=["POST"])
def return_book(book_id):
    book = find_book(book_id)
    if book and book["status"] == "Issued":
        book["status"] = "Available"
    return redirect(url_for("home"))


@app.route("/api/books")
def api_books():
    return {"books": BOOKS}


@app.route("/health")
def health():
    return {"status": "ok"}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
