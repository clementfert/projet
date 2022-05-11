from flask import Flask, render_template, request
from bitcoin import recherche,connexion


#from requests import request
#from bitcoin import devise, prix, tableau

app = Flask(__name__)

@app.route('/')	
def add():
    connexion()
    from bitcoin import tableau,tableau_prix
    if tableau != 0: 
        return render_template('add.html',len = len(tableau),  tableau = tableau, tableau_prix = tableau_prix )



@app.route('/login', methods=['GET','POST'])
def login():
    # on recupere les valeur entrer par l'user 
    global crypto_selectionner
    crypto_selectionner = request.form['crypto_selectionner']
    global quantity
    quantity = request.form['quantity']
    
    # on convertie le valeur rentré par l'utilisateur en float  
    try:
        quantity= float(quantity)
    except:
        return render_template('add.html')

    # on verifie si la valeur est bien quantité est bien en float et on lance la recherche sinon on refrech la page  
    if  quantity == float(quantity):

       recherche()
       from bitcoin import info, prix_total, tableau
       while info == False: 
         return render_template('add.html') 
       if info == True:
         return render_template('add_final.html', prix_total = prix_total, quantity = quantity, crypto_selectionner = crypto_selectionner, tableau = tableau )

    else:
        return render_template('add.html')

     


    