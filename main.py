import json
import xml.etree.ElementTree as ET
import math  # calculer la distance GPS (scénario 4)

def charger_donnees():
    # chargement fichier JSON des artisans
    with open('artisans.json', 'r', encoding='utf-8') as f:
        data_artisans = json.load(f)
        artisans = data_artisans['artisans']

    # chargement fichier JSON de géolocalisation
    with open('geolocalisation.json', 'r', encoding='utf-8') as f:
        data_geo = json.load(f)
        villes = data_geo['villes']

    # chargement fichier XML des échanges
    tree = ET.parse('echanges.xml')
    root = tree.getroot()
    echanges = []
    
    for echange in root.findall('echange'):
        echanges.append({
            'id_artisan': int(echange.find('id_artisan').text),
            'objet_requis': echange.find('objet_requis').text,
            'quantite_min': echange.find('quantite_min').text,
            'objet_offert': echange.find('objet_offert').text
        })

    return artisans, villes, echanges

def main():
    artisans, villes, echanges = charger_donnees()

    while True:
        print("RECYCLAGE & ARTISANAT")
        print("1. Recherche par déchet à recycler")
        print("2. Recherche par récompense souhaitée")
        print("3. Fiche complète d'un artisan")
        print("4. Recherche des artisans à proximité (GPS)")
        print("5. Catalogue des objets recyclables par ville")
        print("0. Quitter l'application")
        print("-" * 40)

        choix = int(input("Choisissez un scénario (de 0 à 5) : "))

        if choix == 1:
            # appel à la future fonction scenario_1(artisans, echanges)
            print("\nLancement du Scénario 1...")
            print("Quel objet voulez-vous recycler ?")
            print("1. Bouteilles en PET\n")

        elif choix == 2:
            # scenario_2(artisans, echanges)
            print("\nLancement du Scénario 2...")
            pass

        elif choix == 3:
            # scenario_3(artisans, villes, echanges)
            print("\nLancement du Scénario 3...")
            pass

        elif choix == 4:
            # scenario_4(artisans, villes)
            print("\nLancement du Scénario 4...")
            pass

        elif choix == 5:
            # scenario_5(artisans, villes, echanges)
            print("\nLancement du Scénario 5...")
            pass

        elif choix == 0:
            print("\nFermeture du service. À bientôt !")
            break

        else:
            print("\nErreur : Veuillez entrer un chiffre entre 0 et 5.")

if __name__ == "__main__":
    main()