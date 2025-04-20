print("hello-world S1")


import sqlite3
import os

# Le chemin vers la base partagée (le volume est monté dans /app/data)
db_path = "/app/data/example.db"

# Connexion à la base (elle sera créée si elle n'existe pas)
conn = sqlite3.connect(db_path)
cur = conn.cursor()


# Créer une table
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
)
""")

# Ajouter un utilisateur
cur.execute("INSERT INTO users (name) VALUES (?)", ("Alice",))

# Lire les données
cur.execute("SELECT * FROM users")
rows = cur.fetchall()

print("Contenu de la table 'users' :")
for row in rows:
    print(row)

# Sauvegarder et fermer
conn.commit()
conn.close()