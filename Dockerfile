# Utilise une image officielle Python depuis Docker 
FROM python:3.11-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers du projet dans le conteneur
COPY . /app

# Installer les dépendances Python dans le fichier requirements.txt 
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Instruction Brief Technique

# Créer un fichier hello-world.py avec un script - Déconseillé
# RUN echo 'print("hello-world S1")' > hello-world.py
# Exécuter le script Python lors du démarrage du conteneur
CMD ["python", "hello-world.py"]




# Installer les dépendances SQLite3 pour Python
RUN pip install sqlite3