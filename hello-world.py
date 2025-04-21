print("hello-world S1")


import sqlite3
import os

# Le chemin vers la base partagée (le volume est monté dans /app/data)
# db_path = "/app/data/example.db"

# Connexion à la base (elle sera créée si elle n'existe pas)
#conn = sqlite3.connect(db_path)
##cur = conn.cursor()


# Créer une table
#cur.execute("""
#CREATE TABLE IF NOT EXISTS users (
#    id INTEGER PRIMARY KEY AUTOINCREMENT,
#    name TEXT NOT NULL
#)
#""")

# Ajouter un utilisateur
#cur.execute("INSERT INTO users (name) VALUES (?)", ("Alice",))

# Lire les données
#cur.execute("SELECT * FROM users")
#ows = cur.fetchall()

#print("Contenu de la table 'users' :")
#for row in rows:
#    print(row)

# Sauvegarder et fermer
#conn.commit()
#conn.close()


# Connexion à la base de données (remplace 'ma_base.db' par le nom de ta base)
conn = sqlite3.connect('users.db')

# Création d'un curseur
cur = conn.cursor()

# Nom de la table à supprimer
nom_table = 'ma_table_a_supprimer'

# Exécuter la commande pour supprimer la table
cur.execute(f"DROP TABLE IF EXISTS {nom_table};")

# Sauvegarder les changements
conn.commit()

# Fermer la connexion
conn.close()

print(f"La table {nom_table} a été supprimée.")