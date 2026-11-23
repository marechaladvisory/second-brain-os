# Airtable : analyse de la structure (2026-11-23)

Phase 1 de l'ajout d'Airtable au brain : comprendre la base, sans rien écrire dans Airtable ni dans `brain/`.
Lecture faite avec le connecteur Airtable (lecture seule : schémas, comptages, échantillons).
Aucune adresse mail, aucun téléphone et aucun identifiant n'est recopié ici.

## 1. Ce que voit le connecteur

- **Une seule base est visible : « 🚀Dev Flo 2 »** (`appJh4Mv3oVmstfzW`), avec le droit `create`. Aucun espace de travail n'est visible (`list_workspaces` est vide) : le compte est invité sur cette base seulement.
- **C'est très probablement une copie de développement**, faite par Florian pour construire le skill SAS, et pas la base de production de MA :
  - le nom (« Dev Flo 2 ») ;
  - les « Next steps » s'arrêtent net : dernière création en septembre 2026, dernière modification le **2026-09-11** ;
  - la table « 7-Team (NEW) » a été créée d'un bloc le 2026-09-05 (refonte en cours) ;
  - depuis septembre, seuls le SAS (73 lignes, des tests E2E du 08/10 au 11/11) et une vingtaine de contacts ont bougé.
- **Conséquence** : cette base convient pour comprendre la structure, mais pas comme source continue. Le CRM réel (dans les notes, Armand, Léonie et Tiana y travaillent chaque jour en novembre) n'est pas visible.
- **Confirmé par Guillaume le 2026-11-23** : « Dev Flo 2 » n'est pas la base de production, mais **le schéma et les apprentissages sont les mêmes**. Tout ce document vaut donc pour la production (tables, champs, formats du CR, contraintes de veille). Seuls les chiffres et les dates de ce document viennent de la copie de septembre.
- Usage retenu : « Dev Flo 2 » sert de **base de test** pour construire et évaluer la veille et la lecture en direct (comme le Drive simulé du skill-lab, mais avec de vraies données). La production sert à la passe initiale et à la veille réelle, une fois partagée avec le connecteur.

## 2. Les tables (14 tables, ≈ 10 600 lignes)

| Table | Lignes | Rôle | Intérêt pour le brain |
| --- | --- | --- | --- |
| 4-Contacts | 4 075 | Le cœur du CRM : une ligne par personne, 228 colonnes | **Fort** : colonne `CR` (historique daté des échanges), liens client, organisation et cluster |
| 1-Next steps | 3 140 | Tâches et suivis : un fil par sujet, retours de GM datés | **Très fort** : 703 lignes ont un CR rédigé |
| 5-Organisations | 2 566 | Noms d'organisations reliés aux contacts | Faible : `Secteur`, `Notes` et `Description` sont vides partout |
| 6- Cluster CN | 286 (44 avec une valeur CN27) | Pipeline ChangeNOW par pays ou délégation : valeur, probabilité, produits, priorité 80/20, « philosophie du partenariat » | **Fort** pour [[changenow-cn27]] |
| 2- Bibliothèque et ressources | 145 | Index des livrables et ressources (decks, process, lettres types) | Moyen : pointe vers le Drive |
| 9- Onboarding | 75 | Parcours d'onboarding (tâches, objectifs, livrables) | Moyen : alimente [[process-ma]] |
| 0-SAS de validation | 73 | Sas d'entrée des contacts et organisations (skill SAS, automation) | Aucun en lecture ; c'est le seul point d'écriture prévu |
| 3-Projets | 47 | Ancienne liste de projets (2025 : AFALULA, Louvre), quasi abandonnée | Faible |
| 2 - Clients | 41 | Clients **et** catégories internes (Personnel, Finance, Recrutement, Prospection et Alliance MA, Procédures…) ; 2 lignes parasites (« 95 EUR », « -183 ») | Fort comme table de correspondance avec `clients/` et `projects/` |
| 8- Recrutement | 37 | Écoles et formations (relations école), avec un champ **`Identifiants`** | À **exclure** (identifiants en clair probables) |
| 7-Team / 7-Team (NEW) | 36 + 36 | Équipe MA **et** interlocuteurs côté client (EDL, ChangeNOW, AFALULA, Art Paris…) | Faible, déjà dans `people/` |
| 10 - Evénements | 15 | Liste d'événements (peu remplie) | Faible |
| 11 - Campaigns | 13 | Calendrier éditorial LinkedIn de juin-juillet 2026 | Faible |

Liens principaux : Contact → Organisation, Client (`Client (à utiliser)`), Cluster, Next Steps Commerciales, Team. Next step → Client, Contacts, Team. Cluster → Contacts, Team. Les tables portent un **préfixe numérique** et plusieurs colonnes en double (« 1-Next steps copy », « Team » et « 7-Team (NEW) »).

## 3. Ce que contiennent les données

### 4-Contacts
- Création : 1 885 lignes importées en mars 2025, puis 863 en juin 2025, et environ 100 par mois ensuite.
- Remplissage : 99 % ont une organisation, environ 75 % une fonction, environ 70 % un mail. **≈ 1 300 contacts ont un `CR`** ; la colonne `Historique des interactions` est vide partout.
- Répartition par client : École du Louvre 983, Vivatech 2023 824, ChangeNOW 674, AFALULA 365, Ville de Paris 215, Personnel 162, Marie Claire 86, DeepTech Summit 74 ; 354 sans client.
- Format du `CR` : un journal **antichronologique**, chaque entrée commence par une date courte et des initiales (« 1206 GM : », « 0502 AD : », « 27/01 MB : »). On y trouve le compte rendu du RDV, les relances (WhatsApp, mail, lettre), les consignes de GM, des éléments de biographie et parfois des brouillons de mails. Exemple type : un contact japonais avec 18 mois d'échanges, des montants, des consignes, des prochaines étapes.
- Environ 200 colonnes d'**opérations ponctuelles** : RSVP, lettres et invitations par édition (CN25, CN26, CN27, DTW26, EDL26, VT26, UNESCO…), cases « à supprimer », « temp ». Ce sont les traces des campagnes, pas des faits durables.
- Colonnes à forte valeur, peu remplies : `? GM` (questions de GM), `ODJ Client`, `Priorité MA Alchimie` (stratégie de compte), `mémo 2027`, `Revoir GM`, `Retours GM CN26`, `Objectif du partenariat 26`.
- `TAGS` : 373 contacts seulement (Vivatech 2026, AFALULA 26 relai Station F, CN26/CN27 lettres VIP, Colloque UNESCO Louvre…).
- `Team (Contact)` (qui suit le contact) : renseigné pour 555 contacts (GM 232, Audrey Chazal 120, GM + Armand 91…).

### 1-Next steps
- Rythme : de 40 à 350 créations par mois entre mars 2025 et septembre 2026 (pic de 350 en février 2026).
- 2 515 sont faites (`Done`) et 600 ouvertes.
- Par client : École du Louvre 321, ChangeNOW 282, AFALULA 257, Maréchal Advisory 192, Prospection et Alliance MA 115, DeepTech Summit 91, Fondation Cartier 45, Hopscotch 42, Art Paris 38, WoC 32 ; 1 676 sans client.
- Par équipe : Armand 346, GM 287, Léonie 165, Loïc Lenoir 34, Mauro 32, des membres de l'équipe EDL ; 2 173 sans équipe.
- `Priorité Tâches` sert aussi de **statut de validation** : « ➡️ Validation GM », « ➡️ Retours faits », « ➡️ Ajout », « 🚀 TTU », « 🚂 Suivi », « 💪 Livrables - milestones ».
- Le `CR` d'une tâche est **la boucle de feedback GM ↔ équipe** : retours datés (« GM 8 août 2026 »), règles de forme (« Jamais de texte justifié », « titres 30, corps 16 »), règles de process (« soumettre le package complet d'un seul bloc : lettre + mail d'accompagnement + relance WhatsApp »), règles de voix (« bannir le jargon IA », « Next step flou = pas une next step »). C'est la meilleure source de `context/voice.md`, de [[process-ma]] et de [[playbook-campagne-lettres]].

### 6- Cluster CN (pipeline ChangeNOW)
- Une ligne par pays ou institution : `Value CN26` / `Value CN27`, `% CN27`, `Atterissage proba CN27 value` (formule), `Produits CN27` (Pavillon, Pitch, Dealflow lounge…), `Priorité Commercialisation CN27` (loi 80/20), `🌳 P. Cluster CN27`, `Philosophie du partenariat` et deux champs IA (résumé, accroche), `🥵` (« GM pas à l'aise »).
- Au 2026-09-11 : valeur CN27 cumulée ≈ 857 k€, dont 391 k€ en « 80 - NOW - gros enjeux » (EIC 100 k à 15 %, Taïwan 50 k à 80 %, Italie 50 k, Côte d'Ivoire 50 k, Réunion 40 k, Nouvelle-Calédonie 36 k, Égypte 35 k, Afrique du Sud 30 k à 70 %).
- Le brain (note du 2026-11-18) donne d'autres chiffres plus récents (EIC 50/100 k, Taïwan MoU signé 40 k) : la copie de septembre est **périmée** sur ce point. C'est une raison de plus de lire la base de production.

### 2 - Clients (correspondance avec le brain)
- Déjà dans le brain : ChangeNOW, École du Louvre (EDL), AFALULA, Art Paris, Fondation Cartier, CPM, PEF, WoC, DeepTech Summit / Inskip, Marie Claire, Beaux Arts & Cie, Musée d'Orsay, Ville de Paris, Station F, Gide, Aquila, Davos, Je M'engage pour l'Afrique.
- Absents du brain : **Rovos Rail** (prospect, lettre « transformative journey », août 2026), **KIFF**, **Alchimiste 2031**, **204 FSM et 92 RA**, Hopscotch (une seule mention).
- Catégories internes, à ne pas traiter comme des clients : Personnel, Finance, Procédures, Recrutement, TALENTS, ADVISORY BOARD, Offre MA, Prospection et Alliance MA, déplacement stratégique.

## 4. Données sensibles et règles déjà en place
- À exclure : le champ `Identifiants` de « 8- Recrutement », les mails, téléphones, adresses postales (`Rue`, `Adresse Postale Lettre`, `Mobile`, `Email - Correspondant…`) et les pièces jointes (`Trombinoscope`).
- Les catégories « Personnel » (162 contacts) et « PERSO » sont privées : on les saute, comme les mails privés.
- Le `CR` contient des éléments de biographie (études, origine) : on ne garde que ce qui sert le business.
- Règle AGENTS.md déjà en place : « Email, CRM, payments: read through the connector, do not copy into notes. Store insights only. »
- Hook `guard-connectors.sh` : il bloque déjà, pour Airtable, `delete_*`, `publish_*` et `submit_*` dans tous les cas, et toute écriture (`create_*`, `update_*`, `revert_action`…) en exécution automatique. Le SAS reste possible en interactif seulement. Rien à changer.

## 5. Contraintes techniques pour une veille continue
- **Aucune table n'a de champ « Last modified time »**. Or le connecteur ne filtre ni ne trie que sur des champs réels (pas de formule `LAST_MODIFIED_TIME()` dans `list_records`). `analyze_table` accepte une formule, mais seulement pour regrouper ou compter.
  → Pour une veille fiable par curseur, il faut **ajouter un champ `lastModifiedTime`** (par exemple « Modifié le », qui suit les champs CR, Next steps, Done, Priorité, valeurs) dans 4-Contacts, 1-Next steps et 6- Cluster CN **de la base de production**. Cette écriture de schéma demande l'accord de Guillaume ; elle se fait en interactif ou à la main.
  → Sans ce champ, la seule solution de repli est une relecture large chaque jour, trop coûteuse sur 4 000 contacts.
- Les valeurs `singleSelect` reviennent sous forme d'objets ; les filtres passent par les ID de champ.
- Les tableaux de la table Contacts sont énormes (228 colonnes) : il faut toujours passer `fieldIds` (une dizaine de colonnes utiles).

## 6. Premières pistes pour les 3 volets (à valider)
1. **Intégration initiale** (même méthode que Drive et Gmail : extraction, registre, writer) :
   - on lit les 703 next steps qui ont un CR et les contacts qui ont un CR **et** un client actif ou un suivi par l'équipe, plus le pipeline Cluster CN27 ;
   - on n'importe pas les 4 000 contacts : on enrichit les fiches `people/` et `clients/` existantes, et on crée une fiche seulement pour un interlocuteur qui revient souvent ;
   - les retours de GM vont dans `decisions.md`, `context/voice.md` (proposition, puisque context est canonique), [[process-ma]] et les playbooks.
2. **Connecteur live** (brain-ask) : « où en est X ? », « quel est le pipe CN27 ? » se lisent en direct dans Airtable, avec la date de la donnée.
3. **Veille continue** (brain-watch, section Airtable, chaque matin dans brain-daily) : `list_records` filtré sur « Modifié le » > curseur, pour les 3 tables. Une entrée de file par record modifié, avec la clé `airtable:<recId>@<modifié le>`. On ne lit que la tête du CR (les entrées postérieures au curseur). Curseur `airtable` dans `notes/sync-state.md`.

## 7. Questions bloquantes pour Guillaume
1. **Accès à la base de production** : il faut la partager avec le compte du connecteur Airtable, ou reconnecter le connecteur avec le compte qui la possède. « Dev Flo 2 » reste la base de test (réponse du 2026-11-23 : même schéma, mêmes apprentissages).
2. Peut-on ajouter un champ « Modifié le » (`lastModifiedTime`) dans 4-Contacts, 1-Next steps et 6- Cluster CN de la production ?
3. Périmètre : quelles catégories de « 2 - Clients » exclure en plus de Personnel ? (Finance ? Recrutement ? TALENTS ?)
4. « Plugin » : une veille par le connecteur (comme Gmail) suffit-elle, ou voulez-vous un plugin empaqueté (skill Airtable dédié, à partager avec l'équipe) ?
