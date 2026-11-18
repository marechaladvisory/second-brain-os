# HANDOFF — setup du second brain de Maréchal Advisory (2026-11-18)

Branche : `claude/clever-euler-y95o7a` (repo marechaladvisory/second-brain-os), tout est commité et poussé.
Brain : `brain/` (racine du repo). Skills utilisés : `skill-lab/build/skills/` (brain-setup + `_shared/contracts.md`).
Artefacts du setup : `brain-setup/` (ce dossier).

## Ce qui a été demandé
« Explorer le repo, lancer le setup du second brain sans brain dump, à partir d'une exploration profonde du Google Drive, étape par étape avec des subagents. »
Choix de l'utilisateur au départ :
- brain dans `brain/` de ce repo ;
- seul le dossier mots de passe est exclu ;
- notes en français ;
- Granola en deuxième étape, et comme connecteur.

En cours de route, il a demandé de lancer les subagents plus séquentiellement : 2 au maximum en parallèle.

## État actuel
| Étape | État |
| --- | --- |
| 1. Scaffold `brain.py init brain` | fait |
| 2. Inventaire Drive (métadonnées) | fait : 350 dossiers, 1 431 fichiers ; `brain-setup/inventory/` |
| 3. Lecture profonde, 12 extractions | fait : `brain/raw/2026-11-18-drive-setup/*.md` (lecture seule, source de vérité du setup) |
| 4. Registre des slugs | fait : `brain-setup/registry.md` (projets, wiki, 76 orgs, 60 personnes, ambiguïtés) |
| 5. Écriture (8 writers W1-W7) | fait : 5 context, 20 projets, 76 clients, 60 people, 4 wiki |
| 6. decisions.md (55), notes/ideas.md, hot.md, AGENTS.md (34 lignes), config.md | fait par le coordinateur à partir de `brain-setup/writer-reports/` |
| 7. index + lint | fait : health 99/100, seul avertissement : review dépassée de `clients/ville-de-la-haye.md` (signal réel) |
| 8. Passe Granola | **BLOQUÉE** : le connecteur répond « user has not created a Granola account yet » |

Contrôles faits : aucun email, téléphone, mot de passe, numéro de passeport ni donnée de santé dans les notes. Les candidats sont notés prénom + initiale, uniquement dans les notes de recrutement.

## Méthode (à réutiliser pour Granola ou une nouvelle passe Drive)
1. Inventaire des métadonnées par un agent.
   - Attention : la recherche de dossiers Drive est incomplète, il faut compléter avec des requêtes « in ancestors » et des get_file_metadata. Voir le rapport dans `inventory/`.
2. Extraction par workstream avec le brief `brain-setup/extract-brief.md`, au format fixe et en français.
   - Chaque fait porte sa source, et chaque fait est marqué fait ou hypothèse.
   - L'agent écrit dans son fichier au fil de l'eau.
3. Un registre de slugs canoniques est établi avant toute écriture, pour éviter les doublons.
4. Writers avec le brief `brain-setup/synth-brief.md`. Chaque writer possède une liste de fichiers disjointe ; il n'écrit ni les index, ni decisions, ni hot, ni log. Le coordinateur fait ensuite decisions, ideas, hot, index, lint, log et commit.
5. Leçons apprises :
   - Les limites d'usage de 5 h ont coupé plusieurs fois les agents. On les reprend avec SendMessage : ils gardent leur progression.
   - Pas plus de 2 agents à la fois.
   - Toujours « écrire chaque fichier dès qu'on a la matière ».
   - Collision de slug : un projet et un client ne doivent jamais partager le même nom. Le projet WoC a été renommé `mission-waves-of-change`.

## Prochaines étapes
1. **Passe Granola**, après création du compte sur https://granola.ai/mcp-signup.
   - Lister toutes les réunions.
   - Un agent extrait par période, au format extract-brief, centré sur les mises à jour des entités du registre, en datant chaque fait.
   - Un seul writer intègre ensuite dans les notes existantes. Il cherche d'abord avec `brain.py search`, étend la note existante, et remplace l'ancienne version d'un fait plutôt que de la garder en double. Il met à jour hot.md, decisions.md et log.md.
   - Puis index et lint.
2. **Session de questions (grill mode de brain-setup)** avec Guillaume, une question à la fois, sur les questions ouvertes ci-dessous. Chaque réponse est mise à jour dans la note concernée, avec la source « (Guillaume, 2026-11-xx) ».
3. **Installation et routines** sur sa machine :
   - `skill-lab/build/install.sh` ;
   - ouvrir `brain/` dans Claude Code ;
   - programmer brain-daily (07:30) et brain-lint (vendredi 16:00) comme indiqué dans `skill-lab/build/INSTALL.md` ;
   - puis le test de contexte : « What does my business do and who works there? ».
4. **brain-evals** : écrire 5 cas réels dans `brain/evals.md` après la première semaine d'usage.

## Questions ouvertes (aussi dans hot.md et dans les notes)
- Honoraires réellement facturés :
  - ChangeNOW CN25-CN27 (le montant de 171 375 € pour CN26 est une valorisation interne, pas une facture), et acceptation ou non d'un retainer ;
  - PEF, GOA, WoC, CPM ;
  - taux de commission AP27 et EDL ;
  - pour EDL : commission seule ou 800 €/mois + commission ?
- Cotonou : quel prix a été envoyé, 76 150 € ou 88 250 € HT ? Le contrat est-il signé ?
- Statut contractuel d'Armand Dogra, Léonie Vankemmel, Virginie Augagneur et Tiana. Qui reprend les dossiers de Léonie à son départ mi-décembre (EDL, AP27, CPM, WoC, GOA, Friendship) ?
- Date de fondation : 2023, ou « 10 ans de MA » avec une soirée le 18/12/2026 ?
- Choix fait après l'entretien final Founder's Associate du 16/11.
- Résultats de l'inauguration de l'amphi Louise Bourgeois (17/11), du RDV Dentressangle et de la visite CPM du 16/11.
- MoU tripartite PEF x B&V x MA : signé ou non ?
- Liste complète des contradictions : section « Questions ouvertes » de chaque note, et `brain-setup/writer-reports/`.

## À signaler à Guillaume (actions dans le Drive)
- Retirer les identifiants en clair de « MA - PROCESS », « WIP - Recrutement WoC - Juillet 2026 » et « MA - Recrutement Janvier 2027 - Mail » ; dossier « Wifi & Mdp » (EDL).
- Retirer les numéros de passeport des lettres visa ChangeNOW (Archives CN24/CN25).
- Fichier personnel « Temps passé au 13 février 2024.xlsx » rangé dans le dossier CTA.
- Ne pas vider « ChangeNOW/1- A SUPPRIMER » : « CR Change now.docx » est la seule trace du contrat 2023.

## Trous connus dans la lecture
- ChangeNOW Toolkit : 4 pptx CN24 de plus de 50 Mo illisibles, 6 « Package » CN26 non ouverts (même gabarit).
- Anciens clients : 75 documents tiers non ouverts (propositions d'agences, rapports externes) ; liste dans `raw/.../anciens.md`.
- Rapports annuels lourds sautés : AXA, CPM 2024, Fondation Société Générale.
- Le détail est dans la section « Inventaire lu » de chaque extraction.
