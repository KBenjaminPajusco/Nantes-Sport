# 🐘 Nantes Sport

Le calendrier de **tous les événements sportifs à Nantes et dans la métropole**, avec l'**état de la billetterie** : matchs des clubs pro (FC Nantes, HBC Nantes, volley, basket, hockey…), courses à pied, vélo, triathlon, grands événements, tournois amateurs, activités de l'agenda de la Métropole…

👉 **Site : https://benjamin.pajusco.fr/Nantes-Sport/**

Petit frère de [Paris-Sportif](https://github.com/KBenjaminPajusco/Paris-Sportif) : même moteur, données nantaises.

## Fonctionnalités

- **Carte plein écran** : 11 quartiers de Nantes + communes de la métropole en aplats pastel, halos proportionnels à l'affluence, épingles par lieu
- Mode **À voir** (matchs pro, grands événements, grandes courses) ou **Tout le sport** ; onglets par sport, filtre par jour / mois, recherche, tri
- **Billetterie** : badge par événement (*Billetterie ouverte*, *Bientôt en vente*, *Complet*, *Inscriptions ouvertes*, *Dossards épuisés*…) + filtre « 🎟 En vente »
- **Affluence** estimée (jauge 1 à 5, taux de remplissage)
- Fiche détaillée avec lien officiel, ajout Google Agenda, export `.ics`, itinéraire
- Filtres partageables via l'URL, responsive mobile

## Sources des données

| Source | Contenu | Mise à jour |
|---|---|---|
| [Agenda des événements de Nantes Métropole (open data)](https://data.nantesmetropole.fr/explore/dataset/244400404_agenda-evenements-nantes-metropole_v2/) | Événements tagués « Sports » / « Événement sportif » + repêchage par mots-clés ; champs `complet` / `annule` / `reporte` → statut billetterie officiel | Automatique, 3×/jour (GitHub Actions) |
| `data/curated/*.json` | Calendriers des clubs, courses, grands événements, amateur — recherchés sur le web | Manuelle |
| `data/tickets.json` | URL billetteries, règles de mise en vente des clubs, dates d'ouverture des inscriptions | Manuelle, statut recalculé chaque jour |
| `data/attendance.json` | Capacités des salles, affluences moyennes, participants des courses | Manuelle |
| API Ticketmaster Discovery (optionnelle) | Statut officiel onsale / offsale si le secret `TICKETMASTER_API_KEY` est défini | Automatique |

Les dates marquées **« à confirmer »** suivent le calendrier habituel mais n'étaient pas encore officiellement publiées.

## Statut billetterie : comment c'est calculé

Par ordre de priorité (`scripts/tickets.py`, zéro appel IA) :

1. **Open data Nantes Métropole** : l'événement est marqué `complet` ou `reporte` par l'organisateur.
2. **Ticketmaster** (si clé API) : statut officiel + date d'ouverture de la vente.
3. **`data/tickets.json`** : statut recherché (date d'ouverture / de clôture → bascule automatique *Bientôt* → *Ouverte* → *Close*).
4. **Règles club** : match pas encore programmé → *Pas encore en vente* ; sinon vente ouverte N semaines avant.
5. Événement gratuit → *Accès gratuit*.

Le **nombre exact de places restantes n'est pas publié** par les billetteries : c'est un statut, pas un compteur.

## Structure

```
scripts/fetch_opendata.py   # open data Nantes Métropole → data/opendata.json
scripts/build.py            # fusion + dédoublonnage + géoloc + affluence + billetterie → docs/events.json
scripts/affluence.py        # estimation du public attendu
scripts/tickets.py          # statut billetterie / inscriptions
data/curated/*.json         # événements recherchés manuellement
data/venues.json            # coordonnées des lieux
docs/                       # site statique (GitHub Pages)
```

## Ajouter un événement

Ajouter un objet dans un fichier de `data/curated/` :

```json
{
  "title": "HBC Nantes – Montpellier Handball",
  "sport": "Handball",
  "category": "Match pro",
  "competition": "Liqui Moly Starligue – J12",
  "federation": "LNH",
  "date_start": "2027-02-11T20:00",
  "date_end": null,
  "venue": "H Arena",
  "address": "…",
  "city": "Nantes",
  "url": "https://…",
  "price": "Payant",
  "tentative": false,
  "description": "Courte description",
  "tags": ["Masculin"]
}
```

L'équipe qui reçoit est citée **en premier** (`Domicile – Visiteur`) : c'est ce qui permet de rattacher affluence et billetterie au bon club.

Catégories : `Match pro`, `Grand événement`, `Course / épreuve participative`, `Sport entreprise`, `Sport universitaire`, `Tournoi amateur`, `Événement communautaire`, `Spectacle sportif`, `Salon`, `Activité / initiation`.

## En local

```bash
python scripts/fetch_opendata.py && python scripts/build.py
cd docs && python -m http.server 8000
```
