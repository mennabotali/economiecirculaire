# Economie Circulaire

# TP1 Mashup — Recyclage et artisanat

**Disclaimer : Les données d'échange et les récompenses sont des données de **simulation**. Les noms figurant dans la liste des artisans et/ou les entreprises concernées ne participent pas réellement à ce service.**

## 1. Objectif

Ce service local permet à un particulier d'identifier des artisans susceptibles de réutiliser des matériaux, de consulter des récompenses fictives offertes en échange et de rechercher ces propositions par ville. L'application est un **mashup**, car elle combine trois sources distinctes avec des identifiants communs.

## 2. Sources de données

| Source | Format | Informations utilisées |
|---|---|---|
| `artisans.json` | JSON | `id`, `nom`, `specialite`, `ville_id` |
| `echanges.xml` | XML | `id_artisan`, `objet_requis`, `quantite_min`, `objet_offert` |
| `geolocalisation.json` | JSON | `ville_id`, `nom_ville`, `canton`, `latitude`, `longitude` |

Le jeu de données comporte **30 artisans**, **20 propositions d'échanges** et **8 villes**. Chaque proposition de `echanges.xml` se relie à un artisan de `artisans.json` par `id_artisan` ↔ `id`. Chaque artisan se relie à une ville de `geolocalisation.json` par `ville_id`. Dix artisans n'ont pas de proposition enregistrée : le programme les conserve dans l'annuaire et affiche le fait qu'aucun échange n'est disponible.

## 3. Utilisation du service

Placer les quatre fichiers suivants dans **le même dossier** :

```text
projet_mashup/
├── main.py
├── artisans.json
├── echanges.xml
└── geolocalisation.json
```

Dans un terminal, depuis le dossier du projet, exécuter :

```bash
python3 main.py
```

Le programme affiche un menu interactif. Entrer un chiffre de `1` à `5` pour choisir un scénario, puis `0` pour quitter. Aucune bibliothèque externe n'est nécessaire : le script utilise uniquement la bibliothèque standard Python (`json`, `xml.etree.ElementTree`, `math`, `pathlib`, `re`, `unicodedata`).

## 4. Scénarios et sources impliquées

### Scénario 1 — Recherche par déchet

- **Entrée** : nom d'un matériau ou d'un déchet, par exemple `bouteille vide`.
- **Sources** : `echanges.xml` (matériau accepté, quantité minimale, récompense) + `artisans.json` (identification et nom de l'artisan).
- **Traitement** : recherche des propositions contenant les mots saisis, puis jointure sur l'identifiant de l'artisan.
- **Sortie** : liste des artisans correspondants, objets demandés, quantités minimales et récompenses.
- **Exemple** : `bouteille vide` affiche « Atelier du Verre – Wilma Besson », avec 10 bouteilles en verre coloré vides demandées dans les données fictives.

### Scénario 2 — Recherche par récompense

- **Entrée** : récompense souhaitée, par exemple `tasse`.
- **Sources** : `echanges.xml` (récompenses et conditions) + `artisans.json` (noms des artisans).
- **Traitement** : filtrage des récompenses et jointure sur `id_artisan` ↔ `id`.
- **Sortie** : artisan proposant la récompense, objet demandé en échange, quantité minimale.
- **Exemple** : `tasse` affiche « Danielle Adjoubel » et la proposition fictive associée à cinq assiettes en faïence.

### Scénario 3 — Fiche d'un artisan

- **Entrée** : identifiant numérique (`id`) d'un artisan, par exemple `1`.
- **Sources** : `artisans.json` (profil) + `geolocalisation.json` (ville et coordonnées) + `echanges.xml` (propositions).
- **Traitement** : recherche de l'artisan, jointure avec la ville par `ville_id`, puis liste de ses échanges par `id_artisan`.
- **Sortie** : nom, spécialité, ville, coordonnées GPS du centre-ville et toutes les offres, ou la mention « Aucun échange enregistré ».

### Scénario 4 — Recherche par proximité GPS

- **Entrée** : latitude et longitude, par exemple `46.204391` puis `6.143158`.
- **Sources** : `geolocalisation.json` (coordonnées des villes) + `artisans.json` (artisans présents) + `echanges.xml` (artisans avec une proposition active dans les données).
- **Traitement** : calcul de la distance à vol d'oiseau par la formule de Haversine jusqu'aux centres des huit villes, sélection de la ville la plus proche, puis jointure avec les artisans de cette ville et leurs propositions.
- **Sortie** : ville la plus proche dans le jeu de données, distance approximative jusqu'à son centre, artisans avec une proposition.
- **Limite** : la proximité concerne le **centre-ville**, pas l'adresse précise de l'atelier. Elle ne garantit pas l'existence d'un artisan proche des coordonnées saisies.

### Scénario 5 — Catalogue par ville

- **Entrée** : nom d'une ville, par exemple `Genève` ou `Geneve`.
- **Sources** : `geolocalisation.json` (recherche de la ville et de son `ville_id`) + `artisans.json` (artisans de cette ville) + `echanges.xml` (objets acceptés et récompenses).
- **Traitement** : identification de la ville, jointure avec les artisans puis avec leurs propositions d'échange.
- **Sortie** : artisans présents, spécialités, propositions et catalogue sans doublons des matériaux acceptés.

## 5. Choix d'implémentation

- Lecture des fichiers au démarrage avec `json.load` et `ElementTree.parse`.
- Recherches de texte non sensibles à la casse et aux accents ; gestion simple de certains pluriels.
- Contrôle des saisies : menu, identifiants numériques, coordonnées GPS.
- Utilisation de `Path(__file__)` pour retrouver les sources même quand le programme est lancé depuis un autre répertoire.
- Aucun service web externe ni base de données ne sont nécessaires : il s'agit d'un service **local**, conformément au périmètre du TP.

## 6. Limites et améliorations envisagées

1. Les propositions d'échange et récompenses ont été générées pour illustrer le TP ; elles **ne sont pas vérifiées auprès des artisans** et ne doivent pas être présentées comme des offres réelles.
2. Les coordonnées disponibles représentent les centres des villes en question. Pour une application réelle, il faudrait disposer des coordonnées des ateliers.
3. `quantite_min` est du texte (par exemple `10`, `5kg`, `1 lot`). Il serait préférable de séparer la valeur numérique et l'unité avant d'automatiser la vérification d'une quantité apportée.
4. Certaines entrées (verre cassé, touches en ivoire) demanderaient une révision pour des raisons de sécurité et de conformité avant toute utilisation réelle.
5. Les recherches utilisent une correspondance simple de mots, non une classification sémantique des matériaux.

## 7. Conclusion

Le projet répond aux exigences techniques du TP : un programme Python en ligne de commande, trois sources distinctes dont JSON et XML, et cinq scénarios d'utilisation. Il démontre plusieurs jointures entre données hétérogènes et une contextualisation spatiale simple par les villes. Les données restent fictives à ce stade.