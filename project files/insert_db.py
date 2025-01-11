import sqlite3
import os

# Path to the database
DB_DIR = "database"
DB_PATH = os.path.join(DB_DIR, "data.db")

# Ensure the directory exists
if not os.path.exists(DB_DIR):
    os.makedirs(DB_DIR)

# Connect to SQLite and create the database
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Create the Queries table
cur.execute("""
CREATE TABLE IF NOT EXISTS Queries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    query TEXT NOT NULL,
    status TEXT NOT NULL,
    image_path TEXT,
    response TEXT
);
""")

# Create the Solutions table
cur.execute("""
CREATE TABLE IF NOT EXISTS Solutions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    image_path TEXT
);
""")

# Insert sample data into Solutions table
sample_data = [
    ("hi", "Hi, how can I help you?", None),
    ("thank you", "Thank you, please let me know if you have any further queries.", None),
    ("What is your refund policy?", "Our refund policy allows returns within 30 days of purchase.", None),
    ("How can I track my order?", "You can track your order using the tracking link in your email.", None),
    ("What payment methods do you accept?", "We accept credit cards, PayPal, and other payment methods.", None),
    ("How do I contact customer support?", "You can contact us via email or our helpline.", None),
    ("Where are you located?", "We are located in New York City.", None),
    ("Do you ship internationally?", "Yes, we ship to most countries worldwide.", None),
    ("What are your working hours?", "Our working hours are 9 AM to 5 PM, Monday to Friday.", None),
    ("How do I reset my password?", "To reset your password, click on 'Forgot Password' on the login page.", None),
    ("What is your return policy?", "You can return items within 30 days with proof of purchase.", None),
    ("How do I cancel my order?", "To cancel your order, please contact customer support.", None),
    ("Do you offer discounts?", "We offer seasonal discounts and promotions.", None),
    ("How can I update my account details?", "You can update your account details in the 'My Account' section.", None),
    ("Is my data secure?", "Yes, we adhere to strict data security standards.", None),
    ("Can I change my delivery address?", "You can change your delivery address before the order is shipped.", None),
    ("What is the warranty on your products?", "Our products come with a 1-year warranty.", None)
]

cur.executemany("INSERT INTO Solutions (question, answer, image_path) VALUES (?, ?, ?)", sample_data)

# Commit and close the connection
conn.commit()
conn.close()

print("Database created and initialized successfully!")
