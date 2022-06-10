
import connexion_mongodb 
import bitcoin 

def porte_feuil():

    #declaration des variable que nous allons utilié pour calculer le gain du porte feuilles de l'user
    gain=0
    gain_total=0
    deficit=0
    deficit_total=0
    global wallet 

    # comparaisson tableau database avec tableau API pour calculer le gain 
    for i,e in enumerate(connexion_mongodb.tableau_menu_name):        
        if e in  bitcoin.tableau:
            print(e)
            print(i)
            for u,x in enumerate(bitcoin.tableau):
                print(u)
                print(x)
                if x==e:
                    gain= bitcoin.tableau_prix[u]-connexion_mongodb.tableau_menu_prix_unitair[i]
                    connexion_mongodb.tableau_gain.append(gain)
                else:
                    print("suivant")

    wallet = sum(connexion_mongodb.tableau_gain)

    return wallet, bitcoin.tableau, bitcoin.tableau_prix,connexion_mongodb.tableau_menu_name, connexion_mongodb.tableau_menu_somme, connexion_mongodb.tableau_menu_quantity, connexion_mongodb.tableau_menu_prix_unitair, connexion_mongodb.tableau_id, connexion_mongodb.tableau_gain