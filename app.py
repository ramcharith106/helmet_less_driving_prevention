from flask import Flask, jsonify, render_template, request
import sqlite3
from datetime import datetime

app = Flask(__name__)

DB_NAME = "violations.db"

# Function to create the database
def create_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Create table if it does not exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS violations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            plate TEXT NOT NULL,
            helmet TEXT NOT NULL CHECK(helmet IN ('Yes', 'No')),
            time TEXT NOT NULL
        )
    """)
    
    conn.commit()
    conn.close()

# Function to fetch all violations
def fetch_violations():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM violations ORDER BY time DESC")
    rows = cursor.fetchall()
    conn.close()

    # Convert fetched data into JSON format
    violations = [{"id": r[0], "plate": r[1], "helmet": r[2], "time": r[3]} for r in rows]
    return violations

# Route to serve the HTML frontend
@app.route("/")
def home():
    return render_template("index.html")

# API Route to fetch violations (Frontend calls this)
@app.route("/api/violations")
def get_violations():
    violations = fetch_violations()
    return jsonify({"data": violations})

# API Route to insert new violations
@app.route("/api/add_violation", methods=["POST"])
def add_violation():
    try:
        data = request.json
        plate = data.get("plate")
        helmet_status = data.get("helmet")

        if not plate or helmet_status not in ["Yes", "No"]:
            return jsonify({"error": "Invalid data"}), 400

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO violations (plate, helmet, time) VALUES (?, ?, ?)",
                       (plate, helmet_status, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        conn.close()

        return jsonify({"message": "Violation added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    create_database()
    print("Database initialized successfully.")
    app.run(debug=True)


