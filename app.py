from flask import Flask, jsonify, request
import mysql.connector
import openai
from taskingai import TaskingAI

app = Flask(__name__)

# Connexion à la base de données MySQL
db = mysql.connector.connect(
  host="localhost",
  user="votre_utilisateur_mysql",
  password="votre_mot_de_passe_mysql",
  database="basket_team"
)

# Configuration de l'API OpenAI
openai.api_key = ''

# Configuration de TaskingAI
taskingai = TaskingAI(model_name="textual-knowledge-gpt-3.5-turbo")

# Fonction pour gérer les demandes de l'utilisateur
def handle_message(message):
    response = taskingai.ask(question=message)
    return response

# Fonction pour récupérer tous les joueurs
@app.route('/api/joueurs', methods=['GET'])
def get_joueurs():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM joueurs")
    result = cursor.fetchall()
    return jsonify(result)

# Fonction pour récupérer un joueur par son ID
@app.route('/api/joueurs/<int:id>', methods=['GET'])
def get_joueur(id):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM joueurs WHERE id = %s", (id,))
    result = cursor.fetchone()
    return jsonify(result)

# Fonction pour ajouter un joueur
@app.route('/api/joueurs', methods=['POST'])
def add_joueur():
    data = request.json
    cursor = db.cursor()
    cursor.execute("INSERT INTO joueurs (nom, position, age, taille, poids) VALUES (%s, %s, %s, %s, %s)", 
                   (data['nom'], data['position'], data['age'], data['taille'], data['poids']))
    db.commit()
    return "Joueur ajouté avec succès"

# Fonction pour mettre à jour un joueur
@app.route('/api/joueurs/<int:id>', methods=['PUT'])
def update_joueur(id):
    data = request.json
    cursor = db.cursor()
    cursor.execute("UPDATE joueurs SET nom = %s, position = %s, age = %s, taille = %s, poids = %s WHERE id = %s", 
                   (data['nom'], data['position'], data['age'], data['taille'], data['poids'], id))
    db.commit()
    return "Joueur mis à jour avec succès"

# Fonction pour supprimer un joueur
@app.route('/api/joueurs/<int:id>', methods=['DELETE'])
def delete_joueur(id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM joueurs WHERE id = %s", (id,))
    db.commit()
    return "Joueur supprimé avec succès"

# Fonction pour récupérer tous les matchs
@app.route('/api/matchs', methods=['GET'])
def get_matchs():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM matchs")
    result = cursor.fetchall()
    return jsonify(result)

# Fonction pour ajouter un match
@app.route('/api/matchs', methods=['POST'])
def add_match():
    data = request.json
    cursor = db.cursor()
    cursor.execute("INSERT INTO matchs (date_match, adversaire, score_equipe, score_adversaire) VALUES (%s, %s, %s, %s)", 
                   (data['date_match'], data['adversaire'], data['score_equipe'], data['score_adversaire']))
    db.commit()
    return "Match ajouté avec succès"

# Fonction pour récupérer tous les entraînements
@app.route('/api/entrainements', methods=['GET'])
def get_entrainements():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM entrainements")
    result = cursor.fetchall()
    return jsonify(result)

# Fonction pour ajouter un entraînement
@app.route('/api/entrainements', methods=['POST'])
def add_entrainement():
    data = request.json
    cursor = db.cursor()
    cursor.execute("INSERT INTO entrainements (date_entrainement, heure_debut, heure_fin, lieu) VALUES (%s, %s, %s, %s)", 
                   (data['date_entrainement'], data['heure_debut'], data['heure_fin'], data['lieu']))
    db.commit()
    return "Entraînement ajouté avec succès"

# Fonction pour récupérer tous les congés
@app.route('/api/conges', methods=['GET'])
def get_conges():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM conges")
    result = cursor.fetchall()
    return jsonify(result)

# Fonction pour ajouter un congé
@app.route('/api/conges', methods=['POST'])
def add_conge():
    data = request.json
    cursor = db.cursor()
    cursor.execute("INSERT INTO conges (date_debut, date_fin, joueur_id, raison) VALUES (%s, %s, %s, %s)", 
                   (data['date_debut'], data['date_fin'], data['joueur_id'], data['raison']))
    db.commit()
    return "Congé ajouté avec succès"

# Fonction pour gérer les messages de l'utilisateur
@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data['message']
    response = handle_message(user_input)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
