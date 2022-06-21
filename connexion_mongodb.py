import flask_pymongo
# partie ajouter la variable denvironnement pour la securité de la base de donné 
import os
from dotenv import load_dotenv
load_dotenv()

def conexion_data_base_crypto ():
    client = flask_pymongo.MongoClient(os.getenv("KEY_DATA_BASE"))
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
    
    return tableau_menu_name, tableau_menu_somme, tableau_menu_quantity, tableau_menu_prix_unitair, tableau_id, tableau_gain



def conexion_data_base_date ():
    #on se connecte à la table contenant la date de notre dernière connexion et la valeur de nos gains 
    from  datetime import date, time, datetime
    from calcul_gain import wallet
    client = flask_pymongo.MongoClient(os.getenv("KEY_DATA_BASE"))
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

    return tableau_date, tableau_y_graphe