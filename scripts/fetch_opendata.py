#!/usr/bin/env python3
"""Récupère les événements sportifs de l'open data de Nantes Métropole
(jeu « Agenda des événements de Nantes Métropole ») et les normalise.

Une ligne du jeu = une date d'un événement : on regroupe par id_manif.
Les champs complet / annule / reporte alimentent le statut billetterie.

Sortie : data/opendata.json
"""
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "opendata.json"
API = "https://data.nantesmetropole.fr/api/explore/v2.1/catalog/datasets/244400404_agenda-evenements-nantes-metropole_v2/exports/json"

FIELDS = ["id_manif", "nom", "description_evt", "lieu", "adresse", "code_postal", "ville", "lieu_quartier",
          "date", "heure_debut", "heure_fin", "gratuit", "precisions_tarifs_evt", "complet", "annule", "reporte",
          "date_report", "themes_libelles", "types_libelles", "lien_agenda", "url_site", "lieu_siteweb",
          "media_url", "location_latlong", "organisateurs", "emetteur"]

SPORT_TYPE = "Evénement sportif"
# Mots-clés forts pour repêcher des événements sportifs non tagués « Sports »
KEYWORDS = r"\b(marathon|semi-marathon|trail|triathlon|duathlon|swimrun|tournoi|match|matchs|course à pied|courses? nature|running|corrida|foulées|\d+ ?km|cyclisme|cyclo|vélo ?cross|rugby|football|futsal|basket|handball|volley|natation|escalade|skate|roller|judo|boxe|escrime|tennis|badminton|pétanque|floorball|hockey|athlétisme|gymnastique|kayak|aviron|voile|régate|randonnée|marche nordique|yoga|pilates|fitness|zumba|tai ?chi|qi ?gong|self-défense|arts? martia|karaté|taekwondo|padel|golf|course d'orientation|cross)\b"
NOT_SPORT_TYPES = re.compile(r"Théâtre|Concert|Projection|Exposition|Contes|Conférence|Cirque", re.I)
NOISE = re.compile(r"puzzle|couture|peinture|bourse aux vélos|répar|méditation|chantier participatif|raconte|lecture|conte|vide-grenier|brocante|fest au", re.I)

# (regex, sport) – l'ordre compte : le premier qui matche gagne
SPORT_RULES = [
    (r"marathon|semi-marathon|course à pied|running|\brun\b|jogging|10 ?km|5 ?km|corrida|foulées", "Course à pied"),
    (r"trail", "Trail"),
    (r"triathlon|duathlon|swimrun", "Triathlon"),
    (r"marche nordique|marche sportive|randonnée|\bmarche\b", "Marche"),
    (r"futsal", "Futsal"),
    (r"foot|five ", "Football"),
    (r"rugby", "Rugby"),
    (r"basket", "Basketball"),
    (r"handball|hand-ball", "Handball"),
    (r"volley", "Volley-ball"),
    (r"badminton|\bbad\b", "Badminton"),
    (r"tennis de table|ping", "Tennis de table"),
    (r"padel", "Padel"),
    (r"tennis", "Tennis"),
    (r"natation|piscine|aquagym|nage|aqua", "Natation"),
    (r"roller|skate|glisse|pumptrack", "Roller / Skate"),
    (r"vélo|cyclisme|cyclo|bmx", "Cyclisme"),
    (r"escalade|grimpe|bloc", "Escalade"),
    (r"judo|karaté|karate|kung fu|wing-tsun|wing tsun|taekwondo|aïkido|aikido|jiu|self[- ]d[ée]fense|arts? martia", "Arts martiaux"),
    (r"boxe|mma|mixed martial|lutte|cardio boxing", "Boxe / Sports de combat"),
    (r"escrime|sabre|fleuret", "Escrime"),
    (r"capoeira", "Capoeira"),
    (r"yoga|pilates|stretching|gym douce|qi ?gong|tai[- ]chi", "Yoga / Bien-être"),
    (r"zumba|fitness|cross ?training|remise en forme|cardio|musculation|renforcement|ppg|préparation physique|abdos|street workout|hiit", "Fitness"),
    (r"gym|motricité|éveil|baby", "Gymnastique / Motricité"),
    (r"pétanque|boule", "Pétanque"),
    (r"parkour", "Parkour"),
    (r"danse|dancehall|hip-hop", "Danse"),
    (r"échecs", "Échecs"),
    (r"golf", "Golf"),
    (r"aviron|kayak|canoë|paddle|voile", "Nautisme"),
    (r"équitation|cheval|hippi", "Équitation"),
    (r"multisport|multi-sport|initiation sportive|sport famille", "Multisports"),
]


def fetch(where: str) -> list:
    params = {"where": where, "select": ",".join(FIELDS), "limit": -1}
    url = API + "?" + urllib.parse.urlencode(params)
    last = None
    for attempt in range(5):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "nantes-sport-calendar/1.0"})
            with urllib.request.urlopen(req, timeout=90) as r:
                return json.load(r)
        except Exception as e:  # réseau capricieux : on réessaie
            last = e
            time.sleep(2 ** attempt)
    raise RuntimeError(f"Échec du téléchargement : {last}")


def guess_sport(text: str) -> str:
    t = text.lower()
    for rx, sport in SPORT_RULES:
        if re.search(rx, t):
            return sport
    return "Multisports"


def guess_category(title: str, tags: str, recurring: bool) -> str:
    t = title.lower()
    if re.search(r"marathon|course|courir|run\b|trail|triathlon|foulées|corrida|\d+ ?km", t) and not recurring:
        return "Course / épreuve participative"
    if re.search(r"tournoi|championnat|games|coupe|challenge|compétition", t):
        return "Tournoi amateur"
    if recurring or re.search(r"cours|stage|atelier|séance|initiation|nantes sport", t):
        return "Activité / initiation"
    if "festival" in (tags or "").lower():
        return "Événement communautaire"
    return "Événement communautaire"


def strip_html(s: str | None) -> str:
    if not s:
        return ""
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()


def yes(v):
    return str(v or "").lower() == "oui"


def is_sport(r) -> bool:
    title = r.get("nom") or ""
    if NOISE.search(title):
        return False
    themes = r.get("themes_libelles") or []
    types = r.get("types_libelles") or []
    kw = re.search(KEYWORDS, title.lower())
    if len(types) > 5:  # fiches qui cochent tous les types : on ne garde que si le titre parle de sport
        return bool(kw)
    if "Sports" in themes or SPORT_TYPE in types:
        # exclut les pièces de théâtre / concerts « sur » le sport
        return not (any(NOT_SPORT_TYPES.search(t) for t in types) and not kw)
    if kw and not any(NOT_SPORT_TYPES.search(t) for t in types):
        return True
    return False


def main() -> int:
    today = date.today().isoformat()
    rows = fetch(f'date >= "{today}"')
    groups = {}
    for r in rows:
        if is_sport(r):
            groups.setdefault(r["id_manif"], []).append(r)

    events = []
    for mid, rs in groups.items():
        rs.sort(key=lambda r: (r.get("date") or "", r.get("heure_debut") or ""))
        r0 = rs[0]
        def dt(r, h):
            d = (r.get("date") or "")[:10]
            t = r.get(h)
            return f"{d}T{t}" if t and t != "00:00" else d
        occ = [[dt(r, "heure_debut"), dt(r, "heure_fin")] for r in rs]
        days = sorted({o[0][:10] for o in occ})
        recurring = len(days) > 3
        title = re.sub(r"^\[[^\]]*\]\s*", "", (r0.get("nom") or "").strip())
        lead = strip_html(r0.get("description_evt"))
        types = r0.get("types_libelles") or []
        loc = r0.get("location_latlong") or {}
        upcoming = [r for r in rs if not yes(r.get("annule"))]
        if not upcoming:
            continue
        ticket = None
        if all(yes(r.get("complet")) for r in upcoming):
            ticket = "sold_out"
        elif any(yes(r.get("reporte")) for r in rs):
            ticket = "postponed"
        cat = guess_category(title, " ".join(types), recurring)
        if "Salon" in types:
            cat = "Salon"
        ev = {
            "id": f"nm-{mid}",
            "title": title,
            "sport": guess_sport(title + " " + lead),
            "category": cat,
            "competition": None,
            "federation": None,
            "date_start": occ[0][0],
            "date_end": None if recurring or days[-1] == days[0] else days[-1],
            "recurring": recurring,
            "occurrences": occ[:80] if recurring or len(days) > 1 else [],
            "schedule": None,
            "venue": r0.get("lieu"),
            "address": ", ".join(str(x) for x in [r0.get("adresse"), r0.get("code_postal"), r0.get("ville")] if x),
            "city": r0.get("ville") or "Nantes",
            "quartier": r0.get("lieu_quartier"),
            "lat": loc.get("lat"), "lon": loc.get("lon"),
            "url": r0.get("url_site") or r0.get("lien_agenda") or r0.get("lieu_siteweb"),
            "price": "Gratuit" if yes(r0.get("gratuit")) else "Payant",
            "price_detail": r0.get("precisions_tarifs_evt"),
            "tentative": False,
            "description": lead,
            "tags": [t for t in types if t != SPORT_TYPE][:3],
            "image": r0.get("media_url"),
            "source": "Agenda Nantes Métropole (open data)",
            "source_url": r0.get("lien_agenda"),
            "od_ticket": ticket,
        }
        events.append(ev)

    events.sort(key=lambda e: e["date_start"] or "")
    OUT.write_text(json.dumps(events, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(events)} événements open data écrits dans {OUT.relative_to(ROOT)} ({len(rows)} lignes lues)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
