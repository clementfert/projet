from flask import Flask, render_template
from bitcoin import devise, prix, tableau

app = Flask(__name__)



@app.route('/')	

def addpage():
    return render_template('add.html', crypto = devise, prix_unitaire = prix, choose = tableau )