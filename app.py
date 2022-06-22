from pipes import Template
import io
import base64
#from tkinter import font
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import seaborn as sns
from bson import ObjectId
from flask import Flask, redirect, render_template, request, url_for,send_file
import flask_pymongo
import matplotlib.pyplot as plt
from bitcoin import connexion
import calcul_gain
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
    calcul_gain.connexion_mongodb.conexion_data_base_crypto()
    calcul_gain.bitcoin.connexion()
    calcul_gain.porte_feuil()
    calcul_gain.connexion_mongodb.conexion_data_base_date()    
    return render_template('menu.html',tableau_menu_name=calcul_gain.connexion_mongodb.tableau_menu_name, tableau_menu_somme=calcul_gain.connexion_mongodb.tableau_menu_somme, len = len(calcul_gain.connexion_mongodb.tableau_menu_name), wallet= calcul_gain.wallet, tableau_gain=calcul_gain.connexion_mongodb.tableau_gain)


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
    return render_template('remove.html',tableau_menu_name=calcul_gain.connexion_mongodb.tableau_menu_name, tableau_menu_somme=calcul_gain.connexion_mongodb.tableau_menu_somme, len = len(calcul_gain.connexion_mongodb.tableau_menu_name))
# on recupere form et on supprime dans notre database
@app.route('/remove_data', methods=['GET','POST'])
def remove_data():
    index_supprimer=int(request.form['crypto_selectionner'])
    id = calcul_gain.connexion_mongodb.tableau_id[index_supprimer]
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
    ax=sns.set_context("paper")
    x=calcul_gain.connexion_mongodb.tableau_date
    y=calcul_gain.connexion_mongodb.tableau_y_graphe
    
    sns.lineplot(x,y)
    canvas=FigureCanvas(fig)
    img=io.BytesIO()
    fig.savefig(img)
    img.seek(0)
    return  send_file(img,mimetype='img/png')

if __name__=="__main__":
    app.run(debug=True) 
    



    



