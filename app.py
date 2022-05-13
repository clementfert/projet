
from flask import Flask, render_template, request
import flask_pymongo
from bitcoin import recherche,connexion
import json

global db, collection




app = Flask(__name__)
client = flask_pymongo.MongoClient("mongodb+srv://clement_fert:studi2022@cluster0.99oev.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")


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
    global show_price
    show_price = request.form['show_price']
    # on les converties 
    show_price= float(show_price)
    quantity=float(quantity)
    investisment = show_price*quantity 
    # on envoie les donnés à la base de donné mongodb 
    db = client.dbtestmongo
    collection = db.get_collection("crypto")
    mydict = { "name": crypto_selectionner, "somme": investisment }
    collection.insert_one(mydict)
    # lecture des donnés
    global tableau_menu_name
    tableau_menu_name=[]
    global tableau_menu_somme 
    tableau_menu_somme=[]
    eduardito=collection.find({})
    for  x in eduardito:
        print(x['name'],x['somme'])
        tableau_menu_name.append(x['name'])
        tableau_menu_somme.append(x['somme'])
    print(tableau_menu_name)
    print(tableau_menu_somme)
    




    return render_template('menu.html')
