# Économie Circulaire
# TP1 — Mashup JSON/XML
## Économie circulaire : mise en relation entre particuliers et artisans

**Cours :** Mashup, contextualisation et qualité des services — Université de Genève 2026–2027  
**Étudiante :** Menna Mahmoud  
**Langage utilisé :** Python 3  
**Type d'application :** Service local en ligne de commande

---

## 1. Introduction

Le recyclage et le réemploi permettent de donner une seconde vie à des matériaux ou objets qui auraient autrement été jetés. Cependant, lorsqu'un particulier possède des bouteilles en verre, des chutes de bois ou de vieux objets, il n'est pas toujours évident de savoir qui pourrait les réutiliser et ce qu'il serait possible de recevoir en échange.

L'objectif de ce projet est de développer un petit service local qui met en relation des particuliers souhaitant se débarrasser de certains matériaux et des artisans susceptibles de les valoriser. Par exemple, une personne qui possède des bouteilles en verre peut rechercher un artisan intéressé et consulter la quantité minimale demandée ainsi que la récompense proposée dans les données de démonstration.

Ce projet s'inscrit dans le cadre du TP1 du cours de Mashup. Un **mashup** consiste ici à combiner des informations provenant de plusieurs sources indépendantes afin de produire un résultat utile pour l'utilisateur. Plutôt que de placer toutes les informations dans un seul fichier, le service associe les profils des artisans, les propositions d'échange et les données géographiques.

Le programme est développé en Python et s'utilise dans un terminal. Il propose **six scénarios**, chacun répondant à un besoin différent.

> **Précision sur les données :** les objets acceptés, les quantités et les récompenses constituent des **propositions fictives conçues pour le TP**. Leur présence dans les fichiers ne signifie pas que les artisans cités ont accepté de participer à ce service ou proposent réellement ces échanges.

## 2. Objectifs et conformité aux consignes

Les consignes du TP demandent de créer un service local en Python, pouvant fonctionner en ligne de commande, qui combine **au moins trois sources de données**, dont **au moins un fichier JSON et un fichier XML**. Elles demandent également **au minimum cinq scénarios distincts** et un rapport expliquant l'utilisation du service, les scénarios et les données mobilisées pour chacun d'eux.

Le projet répond à ces exigences de la manière suivante :

| Exigence du TP | Réalisation dans le projet |
|---|---|
| Service local en Python | Script `main.py`, exécuté dans un terminal |
| Au moins trois sources | `artisans.json`, `echanges.xml`, `geolocalisation.json` |
| Au moins un JSON | Deux fichiers JSON |
| Au moins un XML | Un fichier XML |
| Au moins cinq scénarios | Six scénarios accessibles dans le menu |
| Documentation | Présent rapport Markdown |

Le projet vise également à mettre en pratique la lecture de fichiers, les listes et dictionnaires Python, les boucles, les conditions, les jointures par identifiants, le filtrage, le tri et des calculs géographiques simples.

## 3. Organisation du projet

### 3.1. Arborescence

Les fichiers nécessaires au fonctionnement du service sont placés dans le même dossier :

```text
economiecirculaire/
├── main.py
├── artisans.json
├── echanges.xml
├── geolocalisation.json
└── readme.md
```

Le fichier `main.py` rassemble les fonctions de chargement des données, les six scénarios et le menu principal. Il n'est pas nécessaire de séparer le chargement JSON et XML dans plusieurs scripts : les consignes portent sur le nombre et le format des **sources de données**, et non sur le nombre de fichiers Python.

### 3.2. Les trois sources de données

#### Source 1 — `artisans.json`

Ce fichier contient **30 artisans** et leurs informations principales :

| Champ | Type | Description |
|---|---|---|
| `id` | Entier | Identifiant unique de l'artisan |
| `nom` | Chaîne | Nom de l'artisan ou de l'atelier |
| `specialite` | Chaîne | Domaine d'activité |
| `ville_id` | Entier | Identifiant de la ville associée |

Exemple simplifié :

```json
{
  "id": 1,
  "nom": "Atelier du Verre – Wilma Besson",
  "specialite": "Verre et fusing",
  "ville_id": 1
}
```

Les artisans sont regroupés sous la clé principale `artisans`. Le champ `id` permet d'associer un artisan aux propositions d'échange et `ville_id` permet de retrouver sa ville.

#### Source 2 — `echanges.xml`

Ce fichier contient **30 propositions d'échange**, chacune associée à un artisan. Les informations sont organisées en éléments XML :

| Balise | Description |
|---|---|
| `<id_artisan>` | Identifiant de l'artisan concerné |
| `<objet_requis>` | Objet ou matériau recherché |
| `<quantite_min>` | Quantité minimale, conservée comme texte |
| `<objet_offert>` | Objet, service ou bon proposé en récompense |

Exemple :

```xml
<echange>
    <id_artisan>1</id_artisan>
    <objet_requis>Bouteilles en verre coloré vides</objet_requis>
    <quantite_min>10</quantite_min>
    <objet_offert>Dessous de verre en fusing</objet_offert>
</echange>
```

Le champ `quantite_min` est une chaîne de caractères, car les quantités peuvent être exprimées dans des unités différentes (`10`, `5kg`, `500g`, `1 lot`, etc.). Dans la version actuelle, le programme affiche ces quantités mais n'effectue pas de conversion d'unités.

#### Source 3 — `geolocalisation.json`

Ce fichier contient **8 villes** situées dans les cantons de Genève et de Vaud.

| Champ | Type | Description |
|---|---|---|
| `ville_id` | Entier | Identifiant unique de la ville |
| `nom_ville` | Chaîne | Nom de la ville |
| `canton` | Chaîne | Code du canton (`GE` ou `VD`) |
| `latitude` | Nombre décimal | Latitude du point géographique enregistré |
| `longitude` | Nombre décimal | Longitude du point géographique enregistré |

Exemple :

```json
{
  "ville_id": 1,
  "nom_ville": "Genève",
  "canton": "GE",
  "latitude": 46.204391,
  "longitude": 6.143158
}
```

Ces coordonnées correspondent à des **points de référence des villes** et non à la position exacte de chaque atelier.

### 3.3. Relations entre les sources

Le service relie les fichiers grâce à deux correspondances :

```text
artisans.json                  echanges.xml
     id          =             id_artisan

artisans.json                  geolocalisation.json
   ville_id      =                ville_id
```

Par exemple, l'artisan ayant `id = 1` est relié à l'échange dont `id_artisan = 1`. Son champ `ville_id = 1` renvoie ensuite à la ville de Genève dans `geolocalisation.json`.

Le croisement de ces informations permet de connaître **qui peut récupérer quoi, dans quelle ville et contre quelle récompense**. Dans le jeu de données utilisé, les 30 artisans disposent chacun d'une proposition d'échange associée.

## 4. Fonctionnement technique

### 4.1. Chargement des données

La fonction `charger_donnees()` lit les trois fichiers au lancement du programme :

- `json.load()` lit les deux fichiers JSON et récupère les listes sous les clés `artisans` et `villes` ;
- `xml.etree.ElementTree.parse()` lit le fichier XML ;
- une boucle sur `root.findall('echange')` extrait chaque proposition et la transforme en dictionnaire Python ;
- la fonction renvoie `artisans`, `villes` et `echanges`.

Les données sont ainsi chargées une fois en mémoire, puis transmises aux fonctions des scénarios. Les recherches ne nécessitent pas de rouvrir les fichiers à chaque demande.

### 4.2. Structure générale de `main.py`

Le programme contient les fonctions suivantes :

| Fonction | Rôle |
|---|---|
| `charger_donnees()` | Lire et préparer les données des trois sources |
| `scenario_1()` | Rechercher par déchet à recycler |
| `scenario_2()` | Rechercher par récompense souhaitée |
| `scenario_3()` | Afficher une fiche complète d'artisan |
| `scenario_4()` | Rechercher des artisans dans un rayon géographique |
| `scenario_5()` | Générer le catalogue d'une ville |
| `scenario_6()` | Calculer les statistiques du réseau |
| `main()` | Afficher le menu et exécuter le scénario choisi |

La fonction `main()` utilise une boucle `while True` afin que l'utilisateur puisse effectuer plusieurs recherches successives. Le choix `0` termine l'application. Les choix du menu sont récupérés avec `input()` et comparés aux chaînes de caractères `"1"`, `"2"`, etc.

## 5. Utilisation du service

### 5.1. Prérequis

Le programme utilise **Python 3** ainsi que trois modules de sa bibliothèque standard : `json`, `xml.etree.ElementTree` et `math`. Il ne nécessite aucune bibliothèque tierce ni connexion Internet pour effectuer les recherches sur les fichiers locaux.

### 5.2. Démarrage

1. Placer `main.py`, `artisans.json`, `echanges.xml` et `geolocalisation.json` dans le même dossier.
2. Ouvrir un terminal dans ce dossier.
3. Exécuter :

```bash
python3 main.py
```

Le menu s'affiche :

```text
Économie circulaire : artisanat
1. Recherche par déchet à recycler
2. Recherche par récompense souhaitée
3. Fiche complète d'un artisan
4. Recherche les artisans à proximité
5. Catalogue des objets recyclables par ville
6. Affichage des statistiques du réseau de recyclage
0. Quitter l'application
```

L'utilisateur saisit le numéro du scénario. Après l'affichage du résultat, le menu réapparaît. Pour quitter, il suffit de saisir `0`.

**Remarque :** les fichiers sont actuellement ouverts avec des chemins relatifs (`artisans.json`, par exemple). Il faut donc lancer la commande depuis le dossier du projet, ou adapter ces chemins.

## 6. Description détaillée des six scénarios

### 6.1. Scénario 1 — Recherche par déchet à recycler

**Objectif :** permettre à un particulier de trouver quels artisans pourraient récupérer un objet qu'il possède.

**Saisie de l'utilisateur :** un nom ou quelques mots décrivant le déchet, par exemple `bouteille vide`.

**Sources mobilisées :**

- `echanges.xml` : champ `objet_requis`, `id_artisan`, `quantite_min` et `objet_offert` ;
- `artisans.json` : champs `id`, `nom` et `specialite`.

**Traitement :** la fonction `scenario_1()` parcourt les échanges et vérifie si les mots saisis apparaissent dans la description de l'objet recherché. Pour chaque correspondance, elle retrouve l'artisan avec `artisan['id'] == echange['id_artisan']`, affiche ses informations et incrémente un compteur.

**Exemple :**

```text
Quel objet voulez-vous recycler ? bouteille vide

Artisan 1 : Atelier du Verre – Wilma Besson
Spécialité : Verre et fusing
Objet demandé : Bouteilles en verre coloré vides
Quantité minimale : 10
Récompense : Dessous de verre en fusing

Nombre total d'artisans trouvés reprenant cet objet : 1
```

**Résultat :** liste des propositions correspondantes, avec le nom de l'artisan, la quantité minimale et la récompense. Si aucun résultat n'est trouvé, un message spécifique apparaît.

### 6.2. Scénario 2 — Recherche par récompense souhaitée

**Objectif :** effectuer la recherche inverse du scénario 1 : partir de ce que l'utilisateur aimerait recevoir pour découvrir ce qu'il devrait apporter.

**Saisie de l'utilisateur :** une récompense recherchée, par exemple `tasse`.

**Sources mobilisées :**

- `echanges.xml` : recherche dans `objet_offert`, puis lecture de `objet_requis`, `quantite_min` et `id_artisan` ;
- `artisans.json` : identification du nom et de la spécialité de l'artisan.

**Traitement :** `scenario_2()` compare les mots saisis aux descriptions des récompenses, puis effectue la jointure sur l'identifiant de l'artisan. Le nombre de résultats est affiché à la fin de la recherche.

**Exemple :**

```text
Quelle récompense souhaitez-vous obtenir ? tasse

Artisan 24 : Danielle Adjoubel
Spécialité : Décoration sur céramique
Récompense : Tasse en céramique décorée main
Objet à apporter : Assiettes en faïence ébréchées ou cassées
Quantité minimale : 5

Nombre total d'artisans trouvés proposant cette récompense : 1
```

**Résultat :** les offres correspondant à la récompense demandée, accompagnées des conditions d'échange.

### 6.3. Scénario 3 — Fiche complète d'un artisan

**Objectif :** regrouper en une seule fiche toutes les informations disponibles sur un artisan.

**Saisie de l'utilisateur :** l'ID d'un artisan, par exemple `1`.

**Sources mobilisées :**

- `artisans.json` : `id`, `nom`, `specialite`, `ville_id` ;
- `geolocalisation.json` : `ville_id`, `nom_ville`, `canton`, `latitude`, `longitude` ;
- `echanges.xml` : `id_artisan`, `objet_requis`, `quantite_min`, `objet_offert`.

**Traitement :** la fonction recherche d'abord l'artisan par son ID, puis sa ville par `ville_id`, puis l'ensemble des propositions portant son `id_artisan`. C'est un exemple de mashup utilisant **les trois sources simultanément**.

**Exemple :**

```text
Entrez l'ID de l'artisan (1-30) : 1

--- Fiche de l'artisan ---
Artisan 1 : Atelier du Verre – Wilma Besson
Spécialité : Verre et fusing

--- Localisation ---
Ville : Genève
Canton : GE
Latitude : 46.204391
Longitude : 6.143158

--- Proposition d'échange ---
Objet demandé : Bouteilles en verre coloré vides
Quantité minimale : 10
Récompense : Dessous de verre en fusing
```

**Résultat :** une fiche regroupant le profil de l'artisan, sa localisation au niveau de la ville et ses propositions d'échange. Si l'identifiant n'existe pas ou n'est pas numérique, un message d'erreur est affiché.

### 6.4. Scénario 4 — Recherche des artisans à proximité

**Objectif :** aider l'utilisateur à trouver des artisans dans une zone géographique autour de sa position.

**Saisie de l'utilisateur :** latitude, longitude et rayon de recherche en kilomètres.

**Sources mobilisées :**

- `geolocalisation.json` : coordonnées des villes et `ville_id` ;
- `artisans.json` : rattachement des artisans à ces villes ;
- `echanges.xml` : objets recherchés, quantités et récompenses.

**Traitement :** le programme vérifie d'abord que les coordonnées sont numériques, finies et comprises dans les intervalles valides (latitude entre −90 et 90, longitude entre −180 et 180), et que le rayon est positif. Il calcule ensuite les distances entre la position saisie et chaque ville grâce à la **formule de Haversine**. Les villes situées dans le rayon demandé sont conservées et triées par distance croissante. Pour chaque ville retenue, le programme affiche les artisans associés et leurs échanges.

La formule utilise le rayon moyen de la Terre, approximé à **6 371 km**, ainsi que des coordonnées converties en radians avec le module `math`.

**Exemple :**

```text
Entrez votre latitude (ex. 46.204391): 46.204391
Entrez votre longitude (ex. 6.143158): 6.143158
Dans quel rayon souhaitez-vous chercher (km) ? 10
```

Avec ces valeurs, le programme trouve des propositions dans les villes de Genève (0,00 km depuis le point choisi) et de Carouge (environ 2,46 km), soit **10 propositions** dans le jeu de données utilisé.

**Résultat :** des propositions classées selon la distance des villes, avec le nom et la spécialité de chaque artisan, sa ville et les modalités de l'échange.

**Limite :** les distances ne sont **pas** celles jusqu'aux ateliers. Elles sont calculées depuis la position de l'utilisateur jusqu'aux points géographiques des villes enregistrées. Tous les artisans d'une même ville reçoivent donc la même distance approximative. Il ne s'agit pas non plus d'un temps de trajet routier.

### 6.5. Scénario 5 — Catalogue des objets recyclables par ville

**Objectif :** permettre à l'utilisateur d'explorer les possibilités de recyclage enregistrées pour une ville donnée.

**Saisie de l'utilisateur :** nom de ville, par exemple `Genève`.

**Sources mobilisées :**

- `geolocalisation.json` : recherche du nom de ville et récupération de `ville_id` ;
- `artisans.json` : artisans appartenant à cette ville ;
- `echanges.xml` : objets, quantités et récompenses de chaque artisan.

**Traitement :** la fonction retrouve la ville puis tous les artisans associés à son identifiant. Elle parcourt les échanges de chacun, affiche leurs propositions, et ajoute les descriptions des objets requis à un `set()`. Cette structure évite d'afficher plusieurs fois un objet dont la description est strictement identique. La liste récapitulative est ensuite triée par ordre alphabétique avec `sorted()`.

**Exemple :**

```text
Dans quelle ville souhaitez-vous recycler ? Genève

--- Catalogue de recyclage pour Genève ---

Artisan 1 : Atelier du Verre – Wilma Besson
Spécialité : Verre et fusing
Objet demandé : Bouteilles en verre coloré vides
Quantité minimale : 10
Récompense : Dessous de verre en fusing

...

--- Récapitulatif ---
Nombre d'artisans dans cette ville : 8

Objets recyclables :
- Bouteilles en verre coloré vides
- ...
```

**Résultat :** un catalogue présentant les artisans et les matériaux acceptés dans la ville sélectionnée, ainsi qu'un récapitulatif du nombre d'artisans et des descriptions distinctes d'objets.

**Précision :** le « nombre de types d'objets » affiché par le programme représente le nombre de **descriptions textuelles distinctes**, et non un regroupement normalisé par matériau. La recherche du nom de ville ignore les majuscules mais conserve la distinction entre caractères accentués et non accentués.

### 6.6. Scénario 6 — Statistiques du réseau de recyclage

**Objectif :** fournir une vue globale des données et mettre en évidence leur répartition géographique.

**Saisie de l'utilisateur :** aucune saisie supplémentaire n'est demandée après avoir sélectionné l'option `6` du menu. Le programme calcule directement les statistiques. Les consignes du TP n'imposent pas un `input()` distinct pour chaque scénario.

**Sources mobilisées :**

- `artisans.json` : dénombrement des artisans et regroupement par `ville_id` ;
- `geolocalisation.json` : noms des villes, identifiants et cantons ;
- `echanges.xml` : dénombrement des propositions liées aux artisans.

**Traitement :** `len()` calcule les totaux généraux. Des boucles parcourent les villes, les artisans et les échanges afin de construire des dictionnaires de comptage par ville et par canton. Enfin, `sorted()` classe les villes par nombre décroissant d'artisans.

**Exemple de résultat obtenu :**

```text
--- Statistiques du réseau ---
Nombre total d'artisans : 30
Nombre de propositions d'échange : 30
Nombre de villes : 8

--- Répartition par canton ---
GE : 10 artisans, 10 échanges
VD : 20 artisans, 20 échanges

--- Artisans par ville ---
Lausanne : 14
Genève : 8
Carouge : 2
Etoy : 2
Chavannes-près-Renens : 1
Rolle : 1
Premier : 1
Château-d'Oex : 1

Ville avec le plus d'artisans : Lausanne (14 artisans)
```

**Résultat :** une synthèse chiffrée du réseau de démonstration. Ce scénario est différent des autres, car il ne recherche pas un artisan ou un objet précis : il **produit des statistiques** à partir de l'ensemble des sources.

### 6.7. Synthèse des scénarios et des sources impliquées

| Scénario | Entrée | Sources combinées | Sortie principale |
|---|---|---|---|
| 1. Déchet | Texte libre décrivant l'objet | Artisans JSON + Échanges XML | Artisans acceptant cet objet |
| 2. Récompense | Texte libre décrivant la récompense | Artisans JSON + Échanges XML | Récompenses et conditions d'échange |
| 3. Fiche artisan | ID de l'artisan | Les trois fichiers | Profil, ville, GPS et échanges |
| 4. Proximité | Latitude, longitude, rayon | Les trois fichiers | Propositions dans les villes du rayon, classées par distance |
| 5. Catalogue par ville | Nom de la ville | Les trois fichiers | Artisans, objets et récapitulatif local |
| 6. Statistiques | Choix du menu | Les trois fichiers | Totaux, répartition et classement |

## 7. Vérifications et résultats des tests

Les six scénarios ont été exécutés avec les fichiers de données du projet. Les essais suivants illustrent leur fonctionnement :

| Test | Saisie | Résultat observé |
|---|---|---|
| Recherche par déchet | Option 1, `bouteille vide` | Atelier du Verre – Wilma Besson, 1 résultat |
| Recherche par récompense | Option 2, `tasse` | Danielle Adjoubel, 1 résultat |
| Fiche artisan | Option 3, ID `1` | Profil, ville de Genève, coordonnées et échange |
| Recherche GPS | Option 4, `46.204391`, `6.143158`, `10` | 10 propositions à Genève et Carouge |
| Catalogue par ville | Option 5, `Genève` | 8 artisans, leurs échanges et récapitulatif |
| Statistiques | Option 6 | 30 artisans, 30 échanges, 8 villes ; Lausanne en tête |
| Coordonnées GPS incorrectes | Option 4, latitude `999` | Message d'erreur et retour au menu |
| Ville inconnue | Option 5, `Paris` | Message « Aucune ville trouvée avec ce nom. » |

Les scénarios de recherche par texte ignorent les majuscules grâce à `.lower()` et suppriment les espaces superflus grâce à `.strip()`. Les scénarios 3 et 4 interceptent également certaines saisies non numériques avec `try/except ValueError`.

Ces vérifications confirment le fonctionnement des principales fonctionnalités avec le jeu de données actuel. Elles ne remplacent pas des tests automatisés ou une validation de toutes les données réelles.

## 8. Limites et pistes d'amélioration

Le programme constitue un prototype fonctionnel, mais plusieurs aspects pourraient être améliorés :

1. **Données de démonstration :** les échanges, récompenses et quantités ont été imaginés pour le TP. Il faudrait demander l'accord des artisans avant toute utilisation réelle et vérifier leurs activités, coordonnées et conditions de récupération.
2. **Localisation approximative :** les coordonnées sont celles des villes, pas celles des ateliers. Pour un service réel, il faudrait disposer d'adresses d'ateliers fiables, géocoder celles-ci et proposer une recherche par distance réelle ou par temps de trajet.
3. **Recherche textuelle simple :** `all(mot in description for mot in recherche.split())` fonctionne par sous-chaînes. Une recherche telle que `verre` peut aussi trouver `sous-verre`. Le programme ne gère pas systématiquement les synonymes, les fautes de frappe ou la suppression des accents.
4. **Quantités non calculées :** le programme affiche `quantite_min`, mais ne demande pas encore combien d'objets l'utilisateur possède et ne vérifie pas si le seuil requis est atteint.
5. **Catalogue non normalisé :** le `set()` élimine uniquement les descriptions exactement identiques. Une classification par matériaux (verre, bois, métal, céramique, etc.) permettrait un regroupement plus pertinent.
6. **Service en lecture seule :** aucune réservation, confirmation d'échange, mise à jour de stock ou communication avec les artisans n'est actuellement disponible.
7. **Données locales statiques :** les modifications des offres nécessitent de mettre à jour les fichiers. Une base de données ou une interface d'administration serait plus appropriée pour une application plus grande.

Ces limites n'empêchent pas de répondre aux objectifs du TP : le but principal est de démontrer l'association de données JSON et XML à travers plusieurs usages concrets.

## 9. Conclusion et ouverture

Ce projet m'a permis de développer un service local en Python consacré à l'économie circulaire et à la valorisation de matériaux par des artisans. En combinant trois fichiers indépendants, un JSON contenant les artisans, un XML décrivant les échanges et un autre JSON regroupant les villes, le programme fournit des informations qui ne se trouvent pas réunies dans une seule source.

Les six scénarios montrent différentes manières d'utiliser ces données : rechercher un objet ou une récompense, consulter une fiche complète, effectuer une recherche géographique, explorer le catalogue d'une ville ou obtenir des statistiques sur le réseau. Le projet m'a également permis de mettre en pratique la lecture de fichiers JSON/XML, les jointures par identifiants, les boucles, les dictionnaires et les calculs de distance.

Une suite intéressante serait de transformer ce service en une véritable application ou en un site web plus agréable à utiliser. Par exemple, il serait possible de développer une interface avec Streamlit, qui permet de créer une application web interactive directement en Python. Les utilisateurs pourraient saisir leurs objets dans un champ de recherche, filtrer les résultats par matériau et par ville, visualiser les artisans sur une carte et consulter les récompenses sous forme de fiches illustrées. Cette évolution rendrait le service plus intuitif que l'interface en ligne de commande.

À plus long terme, en utilisant des informations vérifiées auprès des artisans et une localisation plus précise, ce prototype pourrait devenir un outil concret pour encourager le réemploi et faciliter les échanges locaux entre particuliers et professionnels de l'artisanat.