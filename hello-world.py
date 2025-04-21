print("hello-world S1")


import sqlite3
import os



# Création/connexion à la base de données SQLite
#db_name = "analyse_ventes.db"
#conn = sqlite3.connect(db_name)
#cursor = conn.cursor()

# 1. Création des tables nécessaires

# Exmeple de création de table 
# Table des Magasins
#cursor.execute('''
#CREATE TABLE IF NOT EXISTS Produits (
 #   ID Magasin produit REAL NOT NULL,
 #   nom TEXT NOT NULL,
 #   prix REAL NOT NULL,
#)
#''')