
import apikey
import requests

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
choice = input("selectioner votre crypto  ")
valeur_indice =0
tableau = []
for x in coins:

    print(x['symbol'],x['quote']['USD']['price'])
    tableau.append(x['symbol']) 
   
print (tableau)

if choice in tableau:

    for i,e in enumerate(tableau):
         if e == choice:
             print (i,e)
             valeur_indice=i
    
    devise = coins[valeur_indice]['symbol']
    prix = coins[valeur_indice]['quote']['USD']['price']
    print (f"{devise}   {prix}")
    print()

