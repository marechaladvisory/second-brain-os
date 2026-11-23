# HANDOFF — second brain de Maréchal Advisory (mis à jour le 2026-11-23)

Branche de travail : **`main`** (créée le 2026-11-18 à la demande de Guillaume). Le travail Gmail du 2026-11-23 (branche `claude/second-brain-gmail-0qsq6q`) est **fusionné dans `main`** le 2026-11-23 (accord de Guillaume).
Brain : `brain/` (racine du repo). Skills utilisés : `skill-lab/build/skills/` (brain-setup + `_shared/contracts.md`).
Artefacts du setup : `brain-setup/` (ce dossier).
`skill-lab/HANDOFF.md` (2026-11-10, autre repo, essai de Florian) est un historique du lab, pas une consigne pour ce brain.

**Ordre de travail : voir « Prochaines étapes » en bas** (liste revue le 2026-11-19).

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
| 8. Passe Granola | **BLOQUÉE** : le connecteur répond « user has not created a Granola account yet » (revérifié le 2026-11-19 à 12:19 UTC) |
| 9. Veille Drive | **faite le 2026-11-18** : skill brain-watch (evals 4/4, essai à blanc puis premier passage réel : 9 entrées en file). Planification : brain-daily fait la veille chaque matin (voir « Veille : état ») |
| 10. Veille Granola | **à faire** quand le compte Granola existe (encore « no account » le 2026-11-23) |
| 11. Gmail (2026-11-23) | **fait** : veille Gmail dans brain-watch §3 (lecture seule, synthèse recrutement), Gmail live dans brain-ask, evals 5/5 (`skill-lab/evals/results/2026-11-23.md`) ; passe initiale sur toute la boîte (début 2026-10-26 → 2026-11-23T08:51Z) : extractions `brain-setup/gmail/extracts/` (A1, A2, B recrutement), un writer unique ; curseur `gmail` posé à la fin de la passe |
| 12. Sécurité injection (2026-11-23) | **fait** : hook `guard-connectors.sh` (bloque toujours envoi/partage/suppression ; lecture seule des connecteurs en exécution automatique) + `protect.sh` étendu à AGENTS.md, CLAUDE.md, .claude/ ; réseau de l'environnement limité |

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

## Airtable : état au 2026-11-23 (lire en premier)
**Demande** : ajouter Airtable comme les autres sources, avec 3 volets : intégration aux données actuelles, connecteur, entrée continue. Choix de Guillaume : « plugin = connecteur » (comme Gmail : lecture live dans brain-ask, veille dans le brain-daily du matin, pas de plugin empaqueté).
**Fait** :
- Analyse de la structure : `brain-setup/airtable/analyse-structure.md`.
- Champ `Modifié le (brain)` (`lastModifiedTime`, colonnes porteuses de sens seulement) ajouté dans 4-Contacts, 1-Next steps et 6- Cluster CN de « Dev Flo 2 » ; filtre et tri vérifiés.
**Base** : le connecteur ne voit que « 🚀Dev Flo 2 » (`appJh4Mv3oVmstfzW`), copie de dev figée au 2026-09-11. Guillaume : « même schéma, mêmes apprentissages » → c'est la base de test.
**Bloquant pour la passe initiale et la veille réelle** : partager la base de production avec le compte du connecteur Airtable, puis y recréer le champ `Modifié le (brain)` (mêmes colonnes, voir §5 de l'analyse).
**Prochaines étapes** :
1. Construire la veille Airtable dans `skill-lab/` (section Airtable de brain-watch, clés `watch_airtable_*` dans config, source `airtable` dans queue.py, clé `airtable:<recId>@<Modifié le>`, evals sur « Dev Flo 2 »).
2. Ajouter la lecture Airtable live dans brain-ask.
3. Passe initiale sur la production, avec la méthode habituelle (extraction, registre, writer).
4. Ajouter le connecteur Airtable à la tâche brain-daily dans l'interface des routines (action de Guillaume).
**Question ouverte** : quelles catégories de « 2 - Clients » exclure en plus de Personnel (Finance, Recrutement, TALENTS) ?

## Gmail : état au 2026-11-23
**Demande** : Gmail à la fois intégré aux données actuelles, comme connecteur live, et comme entrée continue. Choix de Guillaume : connecteur live (pas de plugin empaqueté) ; veille dans le brain-daily du matin (pas de tâche séparée) ; recrutement en synthèse seulement, aucun candidat nommé depuis les mails.
**Boîte** : guillaume.marechal@ (≈ 380 fils, premier message 2026-10-26 ; ≈ 90 fils de recrutement). Les candidatures arrivent sur l'adresse « hello » et JobTeaser, pas dans cette boîte.
**Fonctionnement** : brain-daily rattrape la veille Gmail chaque matin (curseur `gmail` dans `notes/sync-state.md`), file `source: gmail`, clé `gmail:<threadId>@<dernier message>`. Config : Watch section de `context/config.md` (`watch_gmail_*`). `budget_reads` 60 → 80.
**Limites du connecteur trouvées** : pas de recherche à la seconde (`after:<epoch>` ne renvoie rien) → recherche au jour avec un jour de marge + dates via `get_thread METADATA_ONLY` ; pas de `pageToken` (50 fils max) → découper par dates.
**Sécurité (prompt injection)** : les consignes des skills ne suffisent pas, donc limites mécaniques : `brain/.claude/hooks/guard-connectors.sh` câblé dans `.claude/settings.json` (racine) et `brain/.claude/settings.json` ; `protect.sh` ; dans brain-daily, un mail qui change un montant, une condition de contrat ou une coordonnée bancaire, ou qui vient d'un inconnu, n'est jamais appliqué seul. Réseau : environnement « Default » en accès limité (registres de paquets, serveurs MCP). Le skill d'Airtable (SAS) reste utilisable en interactif ; en automatique, seules les lectures passent.
**Action de Guillaume** : ajouter le connecteur **Gmail** à la tâche brain-daily `trig_018EsRWDjMpJCsaZovDs9xYx` dans l'interface des routines (comme Drive le 2026-11-19), après la fusion dans `main`.

## Veille Drive : état au 2026-11-19
**Fonctionnement retenu**
- `brain-daily` fait tout en une session par jour : `watch_interval_hours: 12` dans `brain/context/config.md` → la dernière veille a toujours plus de 18 h le matin → il lance la veille Drive (brain-watch §2), puis intègre la file. Choix de Guillaume le 2026-11-18 pour économiser le quota (le Drive bouge peu : 17 fichiers modifiés un jour chargé).
- La tâche « brain-watch Drive (toutes les 4 h) » `trig_018odBvVmysP8AHxGgdsjprm` est **désactivée** (pas supprimée). La réactiver seulement si Guillaume veut des notes plus fraîches dans la journée.
- Points de reprise : `brain/notes/sync-state.md`, écrits uniquement par `queue.py cursor set` (ne recule jamais). Curseur Drive : 2026-11-18T22:33Z. `brain.py lint` avertit (`watch`) si aucune veille depuis 24 h.

**Tâches planifiées actives** (nouvelle session à chaque déclenchement, environnement env_01HSMxTzPkKCJzHC9NJtexK7)
- `brain-daily` `trig_018EsRWDjMpJCsaZovDs9xYx`, 07:18 Europe/Paris, notification push.
- `brain-lint` `trig_01RgxFgnPQEhNvr9aekLw8Kg`, vendredi 15:49 Europe/Paris, notification push. (Heures décalées de quelques minutes de 07:30/16:00 : les déclenchements pile à l'heure sont souvent retardés.)
- Connecteur Google Drive et repo `marechaladvisory/second-brain-os` ajoutés **par Guillaume dans l'interface des routines le 2026-11-19** (l'outil create_trigger ne peut pas les attacher pour cette organisation ; get_trigger montre le connecteur mais pas les sources).

**Incident du 2026-11-19** : le brain-daily de 07:18 a tourné avant l'ajout du repo. Intégration faite, mais push refusé (403, repo hors sources) → travail perdu avec le conteneur. Rien de cassé : les 9 entrées Drive restent `new` sur `main`.

**Contrôle du 2026-11-19 à 12:19 UTC** : brain-daily et brain-lint actifs (prochains passages 2026-11-20 06:18Z et 14:49Z), connecteur Google Drive présent sur les deux, veille 4 h désactivée ; 9 entrées `new` en file. On laisse le brain-daily de demain les intégrer (pas d'intégration manuelle).

**À vérifier à la prochaine session**
1. Le brain-daily du 2026-11-20 a-t-il poussé ? `git fetch origin main && git log origin/main -3` doit montrer « brain: daily 2026-11-20 », et `python3 brain/queue.py list --status new` doit être vide. Sinon : `list_events` de la session du run (via `get_trigger` → `last_run.session_id`, kinds ["result"]) pour lire le rapport.
2. Le brain-lint du vendredi 2026-11-20 15:49 a-t-il poussé (« brain: lint … ») ?
3. Si une tâche s'arrête sur une demande de permission : seule `Bash(git push:*)` est dans `.claude/settings.json` (une liste plus large a été refusée par le contrôle de sécurité) ; voir avec Guillaume.
4. Conflits signalés par la veille, que brain-daily doit trancher ou remonter : pavillon EIC 40 k€ vs 50 k€ ; PEF « seul deal = Nigeria » vs HK/Égypte 2026 ; Cotonou 69 j vs 60 j ; onglet Automobile du tableur AP27 (« chinois & coréen ») vs décision du 2026-07-27.

**Fichiers clés**
- Skills : source `skill-lab/build/skills/` → copie dans `brain/.claude/skills/` par `./skill-lab/build/install.sh --target brain/.claude/skills --force` (puis supprimer `brain/.claude/skills-backup-*`). Toujours modifier la source, évaluer, puis recopier.
- Evals : `skill-lab/evals/cases.md` (cas 7-9 = veille), `skill-lab/evals/fixtures/drive/` (Drive simulé), résultats `skill-lab/evals/results/2026-11-18.md` ; décisions dans `skill-lab/log.md`.
- `.claude/settings.json` (racine) : règle git push + hook de protection de `brain/` (raw/, archive/ toujours ; context/ pendant les runs automatiques).
- Périmètre : seul le drive partagé « Maréchal Advisory Team » est surveillé (pas « Mon Drive », lu au setup). Exclus : dossier « Wifi & Mdp », titres « CV ».

**Prochaine grosse étape : Granola** (bloqué tant que `mcp__Granola__get_account_info` répond « no account »)
- Ajouter une section « Granola » à brain-watch (search_meetings updated_after=<curseur>, get_meetings par 10, transcription seulement si un détail manque, clé `granola:<id>@<updated>`), des clés Watch dans config (`connectors` contient déjà granola), un cas d'eval simulé, puis appliquer.
- Puis la passe initiale sur tout l'historique (méthode ci-dessous), puis ajouter le connecteur Granola à la tâche brain-daily dans l'interface des routines (à faire par Guillaume).

## PRIORITÉ d'origine (demande de Guillaume, 2026-11-18) : veille Granola + Drive
Granola et Google Drive sont les **deux entrées principales** du brain. Il faut une veille qui prenne en compte chaque nouvelle entrée ou modification.

**Pré-requis bloquant : Granola.** Au 2026-11-18, `mcp__Granola__get_account_info` répond « user has not created a Granola account yet ».
- Guillaume doit créer ou relier son compte sur https://granola.ai/mcp-signup.
- Puis reconnecter le connecteur Granola dans claude.ai (Settings → Connectors) avec le même compte que son app Granola. Une adresse différente est une cause probable.
- Vérifier ensuite avec `get_account_info`, avant toute autre étape.

**Conception proposée** (à valider avec Guillaume, puis à construire dans `skill-lab/` selon les règles du lab : sandbox d'abord, puis evals) :
1. **Points de reprise datés, pas de fenêtre de 24 h.**
   - `brain-daily` lit aujourd'hui « les dernières 24 h » des connecteurs : si une exécution est ratée, des entrées sont perdues.
   - Stocker un horodatage de dernière synchro par connecteur dans un fichier modifiable pendant les exécutions automatiques, par exemple `brain/notes/sync-state.md`. Pas dans `context/`, qui est en lecture seule pendant ces exécutions.
2. **Veille Drive.**
   - Requête : `'0AJFAnfE8WNvjUk9PVA' in ancestors and (modifiedTime > '<horodatage>' or createdTime > '<horodatage>')`.
   - Exclure le dossier `10a4_E3DXcVAn6tCdKqni4jUuMfxyKoC2` (Wifi & Mdp).
   - Ignorer les images et vidéos. Pour un doc déjà connu, ne lire que ce qui a changé.
   - Écrire une entrée de file par doc utile via `queue.py` (source `drive`, certitude, faits, décisions).
3. **Veille Granola.**
   - `search_meetings(updated_after=<horodatage>)`, puis `get_meetings` par lots de 10, et la transcription seulement si un détail manque.
   - Une entrée de file par réunion (source `granola`).
4. **Intégration.**
   - Seul `brain-daily` intègre la file (contracts §6).
   - Modifications à prévoir : les valeurs `drive` et `granola` dans le champ `source` de `queue.py` ; l'étape 1 de `brain-daily` lit les horodatages et non plus 24 h ; mise à jour des horodatages en fin d'exécution réussie.
5. **Planification** : une tâche planifiée cloud (create_trigger, nouvelle session à chaque déclenchement, repo `marechaladvisory/second-brain-os`, connecteurs Google Drive et Granola).
   - Une veille légère toutes les 4 h, qui ne fait que remplir la file.
   - `brain-daily` à 07:30 Europe/Paris, et `brain-lint` le vendredi à 16:00.
   - Le brain est dans le repo, donc la tâche doit pouvoir committer et pousser. Une règle `Bash(git push:*)` dans `.claude/settings.json` commité est nécessaire : `.claude/settings.local.json` n'existe que dans un conteneur.
6. **Rattrapage initial** : au premier lancement, horodatage Drive = 2026-11-18 (date du setup). Pour Granola, tout l'historique (passe initiale décrite ci-dessous).

## Prochaines étapes Gmail (2026-11-23, avant la liste du 2026-11-19)
1. Fait le 2026-11-23 : fusion dans `main` ; consigne de la tâche brain-daily mise à jour (Gmail, lecture seule, connecteur absent = sauté sans avancer le curseur). **Reste à Guillaume** : ajouter le connecteur Gmail à la tâche brain-daily dans l'interface des routines (aujourd'hui seul Google-Drive y est attaché).
2. Le lendemain : vérifier que le brain-daily a poussé, que `queue.py cursor status` montre `gmail` avancé, et qu'aucune tâche n'a été bloquée par le hook (rapport de la session via `get_trigger` → `last_run.session_id`).
3. Conflits ouverts par la passe Gmail (dans les notes, section Questions ouvertes) : flotte Renault 30-40 vs Art Paris 10 (8 max) ; lettres AP27 envoyées à BYD, MG, Xiaomi, Visa, Mastercard, CB, Ardian, Carmignac, Eurazeo malgré les exclusions ; 87 000 visiteurs / 165 galeries vs 90 000 / 170 ; dates CN27 26-27 vs 26-28/04 ; AFALULA ancien client vs demo day du 09/12 ; contact Stellantis ; AXA « interlocuteur unique ». À passer en grill mode avec Guillaume.
4. Propositions pour context/ (non écrites, à valider par Guillaume) : fondation 2023 (deux mails de GM) et sens de la soirée « 10 ans » ; signatures de GM selon les casquettes (MA « CEO and Founder » depuis le 27/10) ; Tiana assistante recrutement depuis le 12/11 ; motifs de voix (voir log de la passe dans le rapport du writer, résumé dans le message de session du 2026-11-23).

## Prochaines étapes (revues le 2026-11-19, dans l'ordre)
1. **Vérifier les tâches planifiées du 2026-11-20** : voir « À vérifier à la prochaine session » ci-dessus (daily poussé, file vide, lint poussé, pas de blocage sur une permission).
2. **Trancher les 4 conflits de la veille** (EIC, PEF, Cotonou, onglet Automobile AP27) : à partir du rapport du brain-daily ; ce qui demande Guillaume passe par l'étape 7.
3. **Débloquer Granola** (action de Guillaume) : compte sur https://granola.ai/mcp-signup, puis reconnecter le connecteur dans claude.ai (Settings → Connectors) avec la même adresse que l'app. Vérifier avec `get_account_info`.
4. **Construire la veille Granola dans `skill-lab/`**, faisable avant le déblocage avec un Granola simulé : section Granola de brain-watch, clés Watch dans config, cas d'eval simulé, evals, puis recopie dans `brain/.claude/skills/` (détail dans « Veille : état », dernier bloc).
5. **Passe Granola initiale**, une fois le compte relié :
   - lister toutes les réunions ;
   - un agent extrait par période, au format extract-brief, centré sur les mises à jour des entités du registre, en datant chaque fait (2 agents au maximum) ;
   - un seul writer intègre ensuite dans les notes existantes : il cherche d'abord avec `brain.py search`, étend la note existante et remplace l'ancienne version d'un fait plutôt que de la garder en double ; il met à jour hot.md, decisions.md et log.md ;
   - puis index et lint, et avancer le curseur Granola.
6. **Ajouter le connecteur Granola à la tâche brain-daily** dans l'interface des routines (action de Guillaume).
7. **Session de questions (grill mode de brain-setup)** avec Guillaume, une question à la fois, sur les questions ouvertes ci-dessous et les conflits de l'étape 2. Chaque réponse est mise à jour dans la note concernée, avec la source « (Guillaume, 2026-11-xx) ».
8. **Nettoyage du Drive** (action de Guillaume) : voir « À signaler à Guillaume ».
9. **brain-evals** : écrire 5 cas réels dans `brain/evals.md` après la première semaine d'usage, puis lancer brain-evals.

Abandonné : l'installation sur la machine de Guillaume (`install.sh`, routines locales). Les routines cloud la remplacent ; le test de contexte « What does my business do and who works there? » peut se faire dans une session cloud.

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
