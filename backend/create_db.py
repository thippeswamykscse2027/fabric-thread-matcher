import sqlite3

conn = sqlite3.connect("threads.db")
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE threads (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    r INTEGER NOT NULL,
    g INTEGER NOT NULL,
    b INTEGER NOT NULL
)
''')

thread_colors = [
    ("DMC 321", 208, 0, 0),
    ("DMC 666", 227, 29, 66),
    ("Anchor 46", 210, 15, 30),
    ("DMC 310", 0, 0, 0),
    ("DMC 5200", 255, 255, 255),
    ("DMC 727", 255, 239, 0)
]

cursor.executemany("INSERT INTO threads (name, r, g, b) VALUES (?, ?, ?, ?)", thread_colors)

conn.commit()
conn.close()

print("threads.db created and populated successfully!")
