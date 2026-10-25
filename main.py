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


def scenario_1(artisans, echanges):
    recherche = input("Quel objet voulez-vous recycler ? ").strip().lower()

    nombre_resultats = 0

    if not recherche:
        print("Veuillez saisir un objet.")
        return

    # parcourt les échanges
    for echange in echanges:
        objet = echange['objet_requis'].lower()

        # vérifie si les mots recherchés correspondent
        if all(mot in objet for mot in recherche.split()):

            # retrouve l'artisan correspondant à cet échange
            for artisan in artisans:
                if artisan['id'] == echange['id_artisan']:

                    print("\nArtisan", artisan['id'], ":", artisan['nom'])
                    print("Spécialité :", artisan['specialite'])
                    print("Objet demandé :", echange['objet_requis'])
                    print("Quantité minimale :", echange['quantite_min'])
                    print("Récompense :", echange['objet_offert'])
                    print("-" * 5)

                    nombre_resultats += 1
                    break

    if nombre_resultats == 0:
        print("Aucun artisan ne récupère cet objet.")
    else :
        print(f"\nNombre total d'artisans trouvés reprenant cet objet : {nombre_resultats}")
        print("-" * 40)


def scenario_2(artisans, echanges):
    recherche = input("Quelle récompense souhaitez-vous obtenir ? ").strip().lower()

    nombre_resultats = 0

    if not recherche:
        print("Veuillez saisir une récompense.")
        return

    # parcourt les échanges
    for echange in echanges:
        recompense = echange['objet_offert'].lower()

        # vérifie si les mots recherchés correspondent
        if all(mot in recompense for mot in recherche.split()):

            # retrouve l'artisan correspondant à cet échange
            for artisan in artisans:
                if artisan['id'] == echange['id_artisan']:

                    print("\nArtisan", artisan['id'], ":", artisan['nom'])
                    print("Spécialité :", artisan['specialite'])
                    print("Récompense :", echange['objet_offert'])
                    print("Objet à apporter :", echange['objet_requis'])
                    print("Quantité minimale :", echange['quantite_min'])
                    print("-" * 5)

                    nombre_resultats += 1
                    break

    if nombre_resultats == 0:
        print("\nMalheureusement, aucun artisan ne propose cette récompense.")
    else : 
        print(f"\nNombre total d'artisans trouvés proposant cette récompense : {nombre_resultats}")
        print("-" * 40)


def scenario_3(artisans, villes, echanges):
    # demande ID de l'artisan
    try:
        id_recherche = int(input("Entrez l'ID de l'artisan (1-30) : "))
    except ValueError:
        print("Erreur : veuillez entrer un nombre entier.")
        return

    artisan_trouve = None

    # recherche artisan dans json
    for artisan in artisans:
        if artisan['id'] == id_recherche:
            artisan_trouve = artisan
            break

    if artisan_trouve is None:
        print("Aucun artisan trouvé avec cet identifiant.")
        return

    print("\n--- Fiche de l'artisan ---")
    print("Artisan", artisan_trouve['id'], ":", artisan_trouve['nom'])
    print("Spécialité :", artisan_trouve['specialite'])

    ville_trouvee = None

    for ville in villes:
        if ville['ville_id'] == artisan_trouve['ville_id']:
            ville_trouvee = ville
            break

    if ville_trouvee is not None:
        print("\n--- Localisation ---")
        print("Ville :", ville_trouvee['nom_ville'])
        print("Canton :", ville_trouvee['canton'])
        print("Latitude :", ville_trouvee['latitude'])
        print("Longitude :", ville_trouvee['longitude'])
    else:
        print("Localisation inconnue.")

    # recherche l'échanges dans le xml
    nombre_echanges = 0

    for echange in echanges:
        if echange['id_artisan'] == artisan_trouve['id']:

            print("\n--- Proposition d'échange ---")
            print("Objet demandé :", echange['objet_requis'])
            print("Quantité minimale :", echange['quantite_min'])
            print("Récompense :", echange['objet_offert'])
            print("-" * 40)

            nombre_echanges += 1

    if nombre_echanges == 0:
        print("\nAucun échange enregistré pour cet artisan.")
        print("-" * 40)


def scenario_4(artisans, villes, echanges):
    # demande coordonnées et rayon
    try:
        latitude = float(input("Entrez votre latitude (ex. 46.204391): "))
        longitude = float(input("Entrez votre longitude (ex. 6.143158): "))
        rayon = float(input("Dans quel rayon souhaitez-vous chercher (km) ? "))

    except ValueError:
        print("Erreur : veuillez entrer des valeurs numériques.")
        return

    if (not math.isfinite(latitude)
            or not math.isfinite(longitude)
            or not math.isfinite(rayon)
            or not -90 <= latitude <= 90
            or not -180 <= longitude <= 180
            or rayon <= 0):
        print("Erreur : coordonnées ou rayon invalides.")
        return

    # recherche des villes situées dans le rayon
    villes_proches = []

    # conversion des coordonnées de l'utilisateur en radians
    lat1 = math.radians(latitude)
    lon1 = math.radians(longitude)

    for ville in villes:
        # conversion des coordonnées de la ville en radians
        lat2 = math.radians(ville['latitude'])
        lon2 = math.radians(ville['longitude'])

        a = (math.sin((lat2 - lat1) / 2)**2 # calcul de la distance (formule de Haversine)
             + math.cos(lat1) * math.cos(lat2)
             * math.sin((lon2 - lon1) / 2)**2)

        distance = 2 * 6371 * math.asin(math.sqrt(min(1, max(0, a))))

        # vérifie si la ville se trouve dans le rayon
        if distance <= rayon:
            villes_proches.append((distance, ville))

    # classe les villes par distance
    villes_proches.sort(key=lambda element: element[0])

    # rcherche les artisans et leurs échanges
    nombre_resultats = 0

    for distance, ville in villes_proches:

        for artisan in artisans:
            if artisan['ville_id'] == ville['ville_id']:

                for echange in echanges:
                    if echange['id_artisan'] == artisan['id']:

                        print("\nArtisan", artisan['id'], ":", artisan['nom'])
                        print("Spécialité :", artisan['specialite'])
                        print("Ville :", ville['nom_ville'])
                        print(f"Distance : {distance:.2f} km")
                        print("Objet demandé :", echange['objet_requis'])
                        print("Quantité minimale :", echange['quantite_min'])
                        print("Récompense :", echange['objet_offert'])
                        print("-" * 5)

                        nombre_resultats += 1

    # affiche le nombre de résultats
    if nombre_resultats == 0:
        print("\nAucun artisan proposant un échange trouvé dans ce rayon.\n")
    else:
        print(f"\nNombre de propositions trouvées : {nombre_resultats}")
        print("-" * 40)


def scenario_5(artisans, villes, echanges):
    recherche = input("Dans quelle ville souhaitez-vous recycler ? ").strip().lower()

    if not recherche:
        print("Veuillez saisir une ville.")
        return

    ville_trouvee = None
    for ville in villes: # recherche la ville dans le json
        if ville['nom_ville'].lower() == recherche:
            ville_trouvee = ville
            break

    if ville_trouvee is None:
        print("Aucune ville trouvée avec ce nom.")
        return

    print("\n--- Catalogue de recyclage pour", ville_trouvee['nom_ville'], "---")
    nombre_artisans = 0
    objets_recyclables = set() #set pour stocker sans doublon

    for artisan in artisans:
        if artisan['ville_id'] == ville_trouvee['ville_id']: # recherche les artisans de cette ville
            nombre_artisans += 1

            print("\nArtisan", artisan['id'], ":", artisan['nom'])
            print("Spécialité :", artisan['specialite'])
            
            nombre_echanges = 0
            for echange in echanges: # recherche les échanges de cet artisan
                if echange['id_artisan'] == artisan['id']:
                    print("Objet demandé :", echange['objet_requis'])
                    print("Quantité minimale :", echange['quantite_min'])
                    print("Récompense :", echange['objet_offert'])
                    print("-" * 5)

                    objets_recyclables.add(echange['objet_requis'])
                    nombre_echanges += 1

            if nombre_echanges == 0:
                print("Aucun échange enregistré.")

    # Affiche le récapitulatif
    print("\n--- Récapitulatif ---")
    print("Nombre d'artisans dans cette ville :", nombre_artisans)
    
    print("\nObjets recyclables :")
    if objets_recyclables:
        for objet in sorted(objets_recyclables):
            print("-", objet)

        print("\nNombre de types d'objets :", len(objets_recyclables))
    else:
        print("Aucun objet recyclable enregistré.")
    
    print("-" * 40)
    

def scenario_6(artisans, villes, echanges):
    # j'ai ajouté ce scénario car je trouvais que le 4 et le 5 se ressemblaient légèrement
    # (mais celui-ci ne prend pas le input de l'utilisateur donc je n'étais pas sûre que ca suive les consignes)
    print("--- Statistiques du réseau ---")
    print("Nombre total d'artisans :", len(artisans))
    print("Nombre de propositions d'échange :", len(echanges))
    print("Nombre de villes :", len(villes))

    # dictionnaires pour les statistiques
    artisans_par_ville = {}
    artisans_par_canton = {}
    echanges_par_canton = {}

    for ville in villes: # on compte les artisans et les échanges par ville
        nombre_artisans = 0
        nombre_echanges = 0

        for artisan in artisans:
            if artisan['ville_id'] == ville['ville_id']:
                nombre_artisans += 1

                for echange in echanges:
                    if echange['id_artisan'] == artisan['id']:
                        nombre_echanges += 1

        artisans_par_ville[ville['nom_ville']] = nombre_artisans # nb d'artisans par ville
        canton = ville['canton'] # addition des résultats par canton

        if canton not in artisans_par_canton:
            artisans_par_canton[canton] = 0
            echanges_par_canton[canton] = 0

        artisans_par_canton[canton] += nombre_artisans
        echanges_par_canton[canton] += nombre_echanges

    # affiche les statistiques par canton
    print("\n--- Répartition par canton ---")

    for canton in artisans_par_canton:
        print(
            canton, ":",
            artisans_par_canton[canton], "artisans,",
            echanges_par_canton[canton], "échanges"
        )

    # classe les villes par nombre d'artisans
    print("\n--- Artisans par ville ---")

    classement = sorted(
        artisans_par_ville.items(),
        key=lambda element: element[1],
        reverse=True
    )

    for ville, nombre in classement:
        print(ville, ":", nombre)

    # affiche la ville avec le plus d'artisans
    if classement:
        ville_max, nombre_max = classement[0]

        print("\nVille avec le plus d'artisans :", ville_max, "(", nombre_max, "artisans )")
        print("-" * 40)


def main():
    artisans, villes, echanges = charger_donnees()

    while True:
        print("\nÉconomie circulaire : artisanat")
        print("1. Recherche par déchet à recycler")
        print("2. Recherche par récompense souhaitée")
        print("3. Fiche complète d'un artisan")
        print("4. Recherche les artisans à proximité")
        print("5. Catalogue des objets recyclables par ville")
        print("6. Affichage des statistiques du réseau de recyclage")
        print("0. Quitter l'application\n")
        print("-" * 40)

        choix = input("Choisissez un scénario (de 0 à 6) : ")

        if choix == "1":
            print("\nLancement du Scénario 1...")
            scenario_1(artisans, echanges)

        elif choix == "2":
            print("\nLancement du Scénario 2...")
            scenario_2(artisans, echanges)

        elif choix == "3":
            print("\nLancement du Scénario 3...")
            scenario_3(artisans, villes, echanges)

        elif choix == "4":
            print("\nLancement du Scénario 4...")
            scenario_4(artisans, villes, echanges)

        elif choix == "5":
            print("\nLancement du Scénario 5...")
            scenario_5(artisans, villes, echanges)

        elif choix == "6":
                    print("\nLancement du Scénario 6...")
                    scenario_6(artisans, villes, echanges)

        elif choix == "0":
            print("\nFermeture du service. À bientôt !")
            break

        else:
            print("\nErreur : Veuillez entrer un chiffre entre 0 et 6.")

if __name__ == "__main__":
    main()