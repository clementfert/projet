
from pipes import Template
import string
from tkinter import E
from flask import Flask, redirect, render_template, request, url_for
import flask_pymongo
from bitcoin import recherche,connexion
import json

global db, collection, gain, deficit, wallet



app = Flask(__name__)
client = flask_pymongo.MongoClient("mongodb+srv://clement_fert:studi2022@cluster0.99oev.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

@app.route('/')
def menu():
        # lecture de notre database mongoDB
    global tableau_menu_name
    tableau_menu_name=[]

    global tableau_menu_somme 
    tableau_menu_somme=[]
    
    global tableau_menu_quantity
    tableau_menu_quantity=[]
    
    global tableau_menu_prix_unitair
    tableau_menu_prix_unitair=[]

 
    db = client.dbtestmongo
    collection = db.get_collection("crypto")
    eduardito=collection.find({})
    for  x in eduardito:
        print(x['name'],x['somme_total'],x['quantité'],x['prix_unitair'])
        tableau_menu_name.append(x['name'])
        tableau_menu_somme.append(x['somme_total'])
        tableau_menu_quantity.append(x['quantité'])
        tableau_menu_prix_unitair.append(x['prix_unitair'])
        

    print(tableau_menu_name)
    print(tableau_menu_somme)
    connexion()
    from bitcoin import tableau,tableau_prix
    print (tableau)
    print (tableau_menu_name)
    print(tableau_prix)
    gain=0
    gain_total=0
    deficit=0
    deficit_total=0

    #for i in tableau_menu_name:
    for i,e in enumerate(tableau_menu_name):        
        if e in  tableau:
            print(e)
            print(i)
            for u,x in enumerate(tableau):
                print(u)
                print(x)
                if x==e:
                    if tableau_prix[u] >= tableau_menu_prix_unitair[i]:
                       gain= tableau_prix[u]-tableau_menu_prix_unitair[i]
                       gain_total=gain_total+ gain
                       print (f"{gain} " )
                    else:
                         deficit = tableau_menu_prix_unitair[i]-tableau_prix[u]
                         deficit_total= deficit_total + deficit 
                         print (f"{deficit} ")
                else:
                    print("suivant")
    
    wallet= gain_total - deficit_total

    return render_template('menu.html',tableau_menu_name=tableau_menu_name, tableau_menu_somme=tableau_menu_somme, len = len(tableau_menu_name), wallet=wallet)



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
