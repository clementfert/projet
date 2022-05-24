
import json
from time import time

def connexion():
  import apikey
  from flask import render_template
  import requests
  global tableau
  global tableau_prix
  
  headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': apikey.key,
  }

  params = {
    'start':'1',
    'limit':'5',
    'convert':'USD'
  }
  url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
  json = requests.get(url,params=params,headers=headers).json()

  coins = json['data']

  valeur_indice =0
  tableau = []
  tableau_prix =[]
  for x in coins:

      print(x['symbol'],x['quote']['USD']['price'])
      tableau.append(x['symbol']) 
      tableau_prix.append(x['quote']['USD']['price'])
    
  print (tableau)
  return tableau, tableau_prix



    





