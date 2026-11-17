# Notes de recherche – clubs pro / haut niveau de Nantes Métropole (saison 2026-27)

Recherche du 2026-11-17. Seuls les matchs **à domicile** à partir du 17/11/2026 sont dans `curated/pro_teams.json` (91 matchs).
Règle : si la date est connue mais pas l'heure → `YYYY-MM-DD` + `tentative: true`.

| Club | Sport | Division 2026-27 | Salle | Matchs dom. | Sources |
|---|---|---|---|---|---|
| FC Nantes | Football M | **Ligue 2 BKT** (relégué de L1 en 2026) | Stade de la Beaujoire | 11 | https://www.fcnantes.com/articles/20262027/calendrier.php ; https://www.foot-direct.com/equipe/fc-nantes |
| FC Nantes féminines | Football F | Arkema Première Ligue + Coupe LFFP | Stade Marcel-Saupin | 7 | https://www.fcnantes.com/feminines/20262027/calendrier_D1F.php ; https://www.jds.fr/artistes/football-club-de-nantes-feminines-31153_N ; programmefoot (Nantes–Lyon 17h Canal+) |
| HBC Nantes | Handball M | Daikin Starligue + EHF Champions League | H Arena (Paris et Montpellier au Hall XXL du Parc des Expos de la Beaujoire) | 10 | https://hbcnantes.com/equipe-professionnelle/calendrier-et-resultats/ ; https://metropole.nantes.fr/actualites/hbc-nantes-gagner-le-titre-n-est-pas-un-objectif-disproportionne |
| Neptunes de Nantes | **Volley F** | Saforelle VOLSTAR (ex-Power 6, élite) | Salle Mangin Beaulieu | 8 | ICS Google du club (lien sur https://www.neptunesvolley.com/calendrier) ; https://www.lnv.fr/d1f/equipes/nantes-3317 |
| Nantes Basket Hermine | Basket M | Élite 2 (ex-Pro B) | Salle métropolitaine de la Trocardière (Rezé) | 15 | https://www.nantes-basket.com/matchs/calendrier/ |
| Corsaires de Nantes | Hockey sur glace M | Division 1 (pas Magnus) | Patinoire du Petit Port | 11 | https://www.corsairesdenantes.fr/calendrier/ |
| Stade Nantais | Rugby M | Nationale 2 | Stade Pascal-Laporte | 6 | Visuel calendrier : https://www.stadenantais.fr/articles/E75A7F49-0047-4C7C-87DE-C9AAC49402F3 |
| Nantes Métropole Futsal | Futsal M | D1 Futsal | Salle Mangin Beaulieu | 8 | https://epreuves.fff.fr/competition/club/582328-nantes-metropole-f/equipe/2026_189693_SESM_1/resultat-calendrier (page JS, lue via navigateur) |
| Nantes ARH | Rink hockey M | Nationale 1 Élite | Complexe sportif du Croissant | 9 (+2 derbies chez l'adversaire) | Visuels calendrier : https://www.nantes-arh.fr/calendrier-n1-%C3%A9lite |
| ALC Bouguenais / AL Saint-Sébastien | Rink hockey M | Nationale 1 Élite | à confirmer | 1 chacun (derbies vs NARH) | même source NARH |
| Hockey Club de Nantes | Hockey sur gazon | Élite (selon agrégateur) | Plaine de jeux de la Colinière | 4 | https://globalsportsarchive.com/team/field_hockey/hc-nantes/67056/ (agrégateur, non officiel) |

## Clubs vérifiés mais non retenus
- **Neptunes de Nantes handball** : section handball en faillite (juillet 2024). Le nom « Neptunes » désigne désormais le volley féminin (inclus ci-dessus). Plus aucun club féminin de handball métropolitain en LBE/D2F trouvé (HBC Nantes F en N2F).
- **Nantes Rezé Métropole Volley (NRMV)** : absent de l'Alterna VOLSTAR et de la VOLSTAR Masculine 2 (liste LNV), club disparu après dépôt de bilan.
- **Volley-Ball Nantes (fém.)** : c'est l'actuel club des Neptunes de Nantes Volley (inclus).
- **Nantes Rezé Basket (NRB, fém.)** : n'est plus en LFB (descendue en NF1 selon Wikipédia, sans confirmation 2026-27). Non inclus.
- **Water-polo** : aucun club de la métropole en Élite M/F 2026-27 (liste FFN des clubs engagés).

## Lacunes / points à surveiller
- **FC Nantes (L2)** : J17 à J33 n'ont qu'une date de week-end (vendredi indicatif). Les horaires seront fixés par la LFP au fil de la saison. Coupe de France : 8e tour à Nueillaubiers (extérieur) le 28/11. Un match à domicile en 32e ou plus loin est à ajouter si le tirage le donne.
- **FC Nantes F** : dates J12 à J21 « à confirmer » par la LFFP. J11 contre Lyon : 17h00 confirmé par programmefoot (Canal+). Le stade de la Coupe LFFP du 9/12 est supposé être Marcel-Saupin.
- **HBC Nantes** : Ligue des champions terminée à la 3e place du groupe B (phase de groupes du nouveau format). Le club est reversé en **barrages de l'EHF European League** (début 2027). Ni le tirage ni les dates ne sont encore connus, donc ces matchs sont à ajouter. Coupe de France : 1/4 à Toulouse (extérieur) le 18/12. Horaires J16 à J30 non fixés (00:00 sur le site). Play-offs ou Final4 éventuels non inclus.
- **H Arena** : adresse approximative (rue André Tardieu, Île de Nantes, à côté du centre commercial Beaulieu).
- **Neptunes** : pas de play-offs inclus (dates inconnues). J12 et J18 sont des journées d'exemption.
- **Nantes Basket Hermine** : numéros de journée absents de la source. Play-offs Élite 2 non inclus.
- **Corsaires** : calendrier publié jusqu'au 6 mars 2027. Play-offs D1 non inclus.
- **Stade Nantais** : horaires non publiés (généralement dimanche 15h en N2, non vérifié). Toutes les dates sont `tentative`. Adresse précise du stade Pascal-Laporte non vérifiée. Phases finales N2 non incluses.
- **Futsal** : la D1 féminine futsal (Nantes Métropole Futsal F, 1re de sa poule) termine sa 1re phase le 28/11 à Rennes. La 2e phase n'est pas publiée, donc aucun match à domicile connu.
- **Rink hockey** : horaires non publiés. Salles de Bouguenais et Saint-Sébastien à confirmer. Les autres matchs à domicile de l'ALC Bouguenais et de l'AL Saint-Sébastien en N1 Élite ne sont pas couverts (pas de calendrier trouvé, à chercher sur rolskanet.fr).
- **Hockey sur gazon** : source = agrégateur uniquement, sans heures. Genre de l'équipe non confirmé (supposé masculin). Prix non communiqué. À vérifier sur le site de la FFH.
- **Prix** : « Payant » par défaut, sans montant vérifié sauf pour le futsal (10 € / 5 €).
