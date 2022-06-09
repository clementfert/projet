from pipes import Template
import io
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import seaborn as sns
from bson import ObjectId
from flask import Flask, redirect, render_template, request, url_for,send_file
import flask_pymongo
import matplotlib.pyplot as plt
from bitcoin import connexion
import json

# partie ajouter la variable denvironnement pour la securité de la base de donné 
from dotenv import load_dotenv
load_dotenv()
import os

global db, collection, gain, deficit, wallet




app = Flask(__name__)

# URL de notre DATABASE

client = flask_pymongo.MongoClient(os.getenv("KEY_DATA_BASE"))

#route menu principal
@app.route('/')
def menu():
    #declaration des tableau que nous allons utilisé et affiché dans le menu    
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

    #declaration des variable que nous allons utilié pour calculer le gain du porte feuilles de l'user
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


    #on se connecte à la table contenant la date de notre dernière connexion et la valeur de nos gains 
    from  datetime import date, time, datetime
    global tableau_y_graphe
    global tableau_date
    tableau_y_graphe = []
    tableau_date = [] 
    db = client.dbtestmongo
    collection = db.get_collection("graphique")
    eduardito=collection.find({})
    for  x in eduardito:
            print(x['date'],x['y_graphe'])
            tableau_date.append(x['date'])
            tableau_y_graphe.append(x['y_graphe'])

    #on declare une variable (la date  d'aujourdhui)
    aujourdhui = date.today()
    aujourdhui = aujourdhui.strftime('%d/%m/%y')

    # on envoie les donnés à la base de donné mongodb si la date est différente de celle de la database
    if aujourdhui != tableau_date[-1]:
        
            db = client.dbtestmongo
            collection = db.get_collection("graphique")
            mydict = { "date": aujourdhui,"y_graphe": wallet }
            collection.insert_one(mydict)
            tableau_y_graphe.append(wallet)
            tableau_date.append(aujourdhui)
        
    return render_template('menu.html',tableau_menu_name=tableau_menu_name, tableau_menu_somme=tableau_menu_somme, len = len(tableau_menu_name), wallet=wallet,tableau_gain=tableau_gain)


#Si l'user selection "ajouter" on se connect à l'API et on afficher la page html contenant un formulaire pour ajouter une cripto 
@app.route('/add', methods=['GET','POST'])	
def add():
    connexion()
    from bitcoin import tableau,tableau_prix
    if tableau != 0:
        return render_template('add.html',len = len(tableau),  tableau = tableau, tableau_prix = tableau_prix  )

#Une fois le formulaire rempli  
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


#Si l'user selection "suprimer"  on afficher la page html contenant un formulaire pour supprimer une cripto de notre gain
@app.route('/remove', methods=['GET','POST'])
def remove():
    return render_template('remove.html',tableau_menu_name=tableau_menu_name, tableau_menu_somme=tableau_menu_somme, len = len(tableau_menu_name))
# on recupere form et on supprime dans notre database
@app.route('/remove_data', methods=['GET','POST'])
def remove_data():
    index_supprimer=int(request.form['crypto_selectionner'])
    id =tableau_id[index_supprimer]
    db = client.dbtestmongo
    collection = db.get_collection("crypto")
    collection.delete_one({ "_id" : ObjectId(id) })
    return redirect('/')


#Si l'user selection le lien du gain  on afficher la page html graphique
@app.route('/page_graphique', methods=['GET','POST'])
def page_graphique():
    return render_template('graphique.html')    
#Creation du graphique 
@app.route('/graphique', methods=['GET','POST'])
def graphique():
    fig,ax= plt.subplots(figsize=(8,8))
    ax=sns.set_style(style="darkgrid")
    x=tableau_date
    y=tableau_y_graphe
    sns.lineplot(x,y)
    canvas=FigureCanvas(fig)
    img=io.BytesIO()
    fig.savefig(img)
    img.seek(0)
    return  send_file(img,mimetype='img/png')

if __name__=="__main__":
    app.run() 
    



    



