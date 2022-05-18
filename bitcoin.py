
from time import time


def recherche():
  import apikey
  from flask import render_template
  import requests
  from app import crypto_selectionner, quantity
  global prix_total
  global info
  global tableau

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
  for x in coins:

      print(x['symbol'],x['quote']['USD']['price'])
      tableau.append(x['symbol']) 
    
  print (tableau)

  if crypto_selectionner in tableau:

      for i,e in enumerate(tableau):
          if e == crypto_selectionner:
              print (i,e)
              valeur_indice=i
      
      devise = coins[valeur_indice]['symbol']
      prix = coins[valeur_indice]['quote']['USD']['price']
      prix_total = float(quantity)
      prix_total = prix * prix_total
      print (f"{devise}   {prix}")
      info=True
      return info
  else:
    info = False
    prix_total = 0
    return info


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


def test_data_graphique():
  import apikey
  import requests

  headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': apikey.key,
  }
  params ={
    'symbol':'BTC',
    'interval':"daily"
  }
  url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/historical'
  json = requests.get(url,params=params,headers=headers).json()

  coins = json['data']
  tableau_evolution = [] 
  for x in coins:
    tableau_evolution.append(x['quotes']['quote']['USD']['open'])
  print(tableau_evolution)
  return tableau_evolution



