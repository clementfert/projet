from flask import Flask, render_template, request
from bitcoin import recherche,connexion
import json
#from flask_mongoengine import MongoEngine

#from requests import request
#from bitcoin import devise, prix, tableau

app = Flask(__name__)

@app.route('/')	
def add():
    connexion()
    from bitcoin import tableau,tableau_prix

    if tableau != 0:

        return render_template('add.html',len = len(tableau),  tableau = tableau, tableau_prix = tableau_prix,  )





@app.route('/login', methods=['GET','POST'])
def login():
    # on recupere les valeur entrer par l'user 
    global crypto_selectionner
    crypto_selectionner = request.form['crypto_selectionner']
    global quantity
    quantity = request.form['quantity']
    return render_template('menu.html')