
from pipes import Template
import string
from tkinter import E
from bson import ObjectId
from flask import Flask, redirect, render_template, request, url_for
import flask_pymongo
from bitcoin import recherche,connexion,test_data_graphique
import json
connexion()
test_data_graphique()
global db, collection, gain, deficit, wallet



app = Flask(__name__)
client = flask_pymongo.MongoClient("mongodb+srv://clement_fert:studi2022@cluster0.99oev.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

@app.route('/')
def menu():
        
    global tableau_menu_name
    tableau_menu_name=[]

    global tableau_menu_somme 
    tableau_menu_somme=[]
    
    global tableau_menu_quantity
    tableau_menu_quantity=[]
    
    global tableau_menu_prix_unitair
    tableau_menu_prix_unitair=[]

    global tableau_id
    tableau_id=[]

    global tableau_gain
    tableau_gain=[]

  # lecture de notre database mongoDB
    db = client.dbtestmongo
    collection = db.get_collection("crypto")
    eduardito=collection.find({})
    for  x in eduardito:
        print(x['_id'],x['name'],x['somme_total'],x['quantité'],x['prix_unitair'])
        tableau_menu_name.append(x['name'])
        tableau_menu_somme.append(x['somme_total'])
        tableau_menu_quantity.append(x['quantité'])
        tableau_menu_prix_unitair.append(x['prix_unitair'])
        tableau_id.append(x['_id'])
        

 #connexion à l'API 
    connexion()
    from bitcoin import tableau,tableau_prix
 
    gain=0
    gain_total=0
    deficit=0
    deficit_total=0

    # comparaisson tableau database avec tableau API pour calculer le gain 
    for i,e in enumerate(tableau_menu_name):        
        if e in  tableau:
            print(e)
            print(i)
            for u,x in enumerate(tableau):
                print(u)
                print(x)
                if x==e:
                   gain= tableau_prix[u]-tableau_menu_prix_unitair[i]
                   tableau_gain.append(gain)
                else:
                    print("suivant")
    
    wallet= sum(tableau_gain)

    return render_template('menu.html',tableau_menu_name=tableau_menu_name, tableau_menu_somme=tableau_menu_somme, len = len(tableau_menu_name), wallet=wallet,tableau_gain=tableau_gain)



@app.route('/add', methods=['GET','POST'])	
def add():
    connexion()
    from bitcoin import tableau,tableau_prix

    if tableau != 0:
        return render_template('add.html',len = len(tableau),  tableau = tableau, tableau_prix = tableau_prix  )




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
    mydict = { "name": crypto_selectionner,"quantité": quantity,"prix_unitair":show_price, "somme_total": investisment }
    collection.insert_one(mydict)
    return redirect('/')


@app.route('/remove', methods=['GET','POST'])
def remove():
    return render_template('remove.html',tableau_menu_name=tableau_menu_name, tableau_menu_somme=tableau_menu_somme, len = len(tableau_menu_name))

@app.route('/remove_data', methods=['GET','POST'])
def remove_data():
    index_supprimer=int(request.form['crypto_selectionner'])
    id =tableau_id[index_supprimer]
    db = client.dbtestmongo
    collection = db.get_collection("crypto")
    collection.delete_one({ "_id" : ObjectId(id) })
    return redirect('/')





