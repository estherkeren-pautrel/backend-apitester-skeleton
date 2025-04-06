import pathlib as pl

import numpy as np
import pandas as pd

from flask import Flask, jsonify, request
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

data = pl.Path(__file__).parent.absolute() / 'data'

# Charger les données CSV
associations_df = pd.read_csv(data / 'associations_etudiantes.csv')
evenements_df = pd.read_csv(data / 'evenements_associations.csv')

## Vous devez ajouter les routes ici : 

@app.route('/api/alive', methods=['GET'])
def check_alive():
    return jsonify({"message": "Alive"}), 200

associations = associations_df.to_dict(orient='records')

@app.route('/api/associations', methods=['GET'])
def get_associations():
    # On ne retourne que les ids des associations
    association_ids = [association["id"] for association in associations]
    
    return jsonify(association_ids), 200 

@app.route('/api/association/<int:id>', methods=['GET'])
def details_association(id):
    for association in associations:
        if id == association["id"]:
            return jsonify(association), 200
    return jsonify({ "error": "Association not found" }), 404

evenements = evenements_df.to_dict(orient='records')

@app.route('/api/evenements', methods=['GET'])
def get_evenements():
    # On ne retourne que les ids des evenements
    evenement_ids = [evenement["id"] for evenement in evenements]
    return jsonify(evenement_ids), 200 

@app.route('/api/evenement/<int:id>', methods=['GET'])
def details_evenement(id):
    for evenement in evenements:
        if id == evenement["id"]:
            return jsonify(evenement), 200
    return jsonify({ "error": "Event not found" }), 404

@app.route('/api/association/<int:id>/evenements', methods=['GET'])
def liste_evenements(id):
    liste = []
    for evenement in evenements:
        if evenement["association_id"] == id:
            liste.append(evenement["nom"])
    return jsonify(liste), 200

"""
@app.route('/api/associations/type/<type>', methods=['GET'])
def types_associations(type):
    liste_types = []
    for association in associations:
        if association["type"] == type:
            liste_types.append(association)
    return jsonify(liste_types), 200
"""


if __name__ == '__main__':
    app.run(debug=False)
