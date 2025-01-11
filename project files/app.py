from flask import Flask, request, render_template, jsonify
import sqlite3

app = Flask(__name__)

# Database setup
DB_PATH = "database/data.db"


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)  # Connect to the database
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries for better handling
    return conn


def query_db(query, args=(), one=False):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(query, args)
    rv = cur.fetchall()
    conn.commit()
    conn.close()
    return (rv[0] if rv else None) if one else rv


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get-response", methods=["POST"])
def get_response():
    user_query = request.json.get("query", "").strip()
    if not user_query:
        return jsonify({"response": "Please provide a valid query."})

    # Search for a solution in the database
    result = query_db("SELECT answer FROM Solutions WHERE question LIKE ?", (f"%{user_query}%",), one=True)
    if result:
        return jsonify({"response": result[0]})
    else:
        # Log the query for support staff and return a generic response
        query_db("INSERT INTO Queries (query, status) VALUES (?, ?)", (user_query, "Pending"))
        return jsonify({"response": "Your query has been logged. Our support staff will get back to you shortly."})


@app.route("/pending-queries", methods=["GET"])
def view_pending_queries():
    pending_queries = query_db("SELECT id, query FROM Queries WHERE status = 'Pending'")
    return render_template("pending_queries.html", pending_queries=pending_queries)


@app.route("/respond-to-query", methods=["POST"])
def respond_to_query():
    query_id = request.form.get("query_id")  # Extract query ID from the form
    response = request.form.get("response")  # Extract the response text from the form

    if not query_id or not response:
        return "Query ID and response are required.", 400

    # First, get the question associated with the query_id
    conn = get_db_connection()
    query = conn.execute("SELECT query FROM Queries WHERE id = ?", (query_id,)).fetchone()
    
    if query is None:
        return "Query not found.", 404

    # Insert the response into the Solutions table
    conn.execute("INSERT INTO Solutions (question, answer) VALUES (?, ?)", (query['query'], response))

    # Update the query status to 'Answered' and store the response in the Queries table
    conn.execute("UPDATE Queries SET status = 'Answered', response = ? WHERE id = ?", (response, query_id))

    conn.commit()
    conn.close()

    return "Response submitted successfully."

@app.route("/submit-responses", methods=["POST"])
def submit_responses():
    # Get all submitted form data
    responses = request.form

    conn = get_db_connection()
    for key, response in responses.items():
        if response.strip():  # Skip empty responses
            # Extract query ID from the textarea name
            query_id = key.split('_')[1]
            
            # Get the original query from the database
            query = conn.execute("SELECT query FROM Queries WHERE id = ?", (query_id,)).fetchone()
            if query:
                # Insert into the Solutions table
                conn.execute("INSERT INTO Solutions (question, answer) VALUES (?, ?)", (query['query'], response))
                # Mark the query as answered
                conn.execute("UPDATE Queries SET status = 'Answered', response = ? WHERE id = ?", (response, query_id))

    conn.commit()
    conn.close()

    return "Responses submitted successfully!"

if __name__ == "__main__":
    app.run(debug=False)
