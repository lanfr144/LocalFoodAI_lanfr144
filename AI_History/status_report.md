# 🏆 Synthèse Agile & Wiki SCRUM

Voici le compte-rendu officiel du projet **Local Food AI**, structuré pour répondre aux exigences des rituels Scrum (Daily, Review, Planning) et pour alimenter directement votre Wiki Taiga.

---

## 1. 🌅 Le Daily (Où en sommes-nous ?)
**Statut Actuel :** 
Le socle applicatif est à 90% terminé. L'infrastructure de base (MySQL, Ubuntu, Docker, Ollama) est parfaitement stable, le pipeline d'intégration Git/Taiga via Webhook est fonctionnel, et l'interface utilisateur (UI) vient de subir une refonte technologique massive. Il ne reste techniquement qu'une seule "Epic/User Story" majeure dans notre Backlog.

---

## 2. 🔍 La Sprint Review (Qu'avons-nous fait hier ?)
Lors du dernier Sprint de développement continu, nous avons validé les User Stories **#5, #6, #7, et #8**. 

**Réalisations Techniques et Démontrables :**
* **Refonte "Scientific Medical" (Frontend) :** Injection de CSS avancé dans `app.py` pour basculer Streamlit vers un design "Dark Mode" Premium, utilisant la police Inter, des dégradés bleus/cyan, et des effets "Glassmorphism".
* **Filtres Avancés (SQL/Backend) :** Création de 4 sliders interactifs (Protéines, Lipides, Glucides, Sucres) modifiant dynamiquement la clause `WHERE ... AND protéines >= X` de la base MySQL.
* **Architecture "My Plate" (Database) :** Modification sécurisée de `setup_db.py` pour générer automatiquement deux nouvelles tables relationnelles (`plates` et `plate_items`). Ces tables utilisent des clefs étrangères (Foreign Keys) pour lier les aliments directement au `user_id` de la session.
* **Algorithme d'Agrégation (Logique Data) :** Intégration d'une logique en Python/Pandas calculant et additionnant instantanément les macros (Protéines, Graisses, Carbs) de tous les aliments présents dans une assiette virtuelle.
* *Toutes ces modifications ont été commitées sur Gogs avec succès, déclenchant le Webhook vers Taiga (Tasks #23, #24, #26, #27).*

---

## 3. 🎯 Le Sprint Planning (Qu'allons-nous faire ?)
**Prochain Objectif :** Construire la **User Story #11 (AI Menu Proposals)**.

**Tâches prévues (Sprint Backlog) :**
1. Créer une nouvelle section/tab dans le code pour la génération de menus.
2. Concevoir un algorithme de "Prompt Engineering" très spécifique qui imposera à **Mistral** des contraintes strictes.
3. Câbler la demande de l'utilisateur (ex: "Je veux un menu à 2000 kcal riche en protéines") avec la base de données SQL locale pour fournir de vrais exemples au LLM, afin qu'il propose un menu concret et non inventé.
4. Finaliser les play-tests finaux sur la VM Ubuntu.

---

## 4. 📚 Ce que tu dois mettre dans le Wiki SCRUM (Taiga)
Copiez-collez ces blocs dans votre Wiki Taiga pour prouver la maîtrise technique du projet :

### 🏛️ Architecture & Technologies
* **Frontend :** Framework **Streamlit** (Python) surchargé par du CSS natif injecté via `st.markdown(unsafe_allow_html=True)` pour garantir une esthétique "Scientific Medical" (Focalisation UX/UI Premium).
* **Backend Intelligence :** Intégration native de l'API **Ollama (modèle Mistral)** avec le concept de *Tool/Function Calling* pour scraper anonymement le Web via un conteneur local **SearXNG** sur le port `8080`.
* **Database Pipeline :** Injection dynamique et asynchrone des données CSV ouvertes via Pandas vers MySQL. Abandon des schémas SQL rigides au profit de l'auto-génération des 200 colonnes via l'ORM.
* **Sécurité & Accès :** Mise en place d'un modèle **PoLP** (Principle of Least Privilege). L'application gère nativement le HMAC (via `bcrypt`) et le script `setup_db.py` octroie des droits granulaires (ex: `IDENTIFIED BY ... GRANT SELECT, INSERT... TO 'db_app_auth'`).

### 🔄 DevOps & Déploiement
* Le CI/CD rudimentaire repose sur une intégration **Gogs -> Taiga**. Chaque commit (ex: `TG-23`) documente automatiquement la carte Agile via Webhook.
* Le système est déployable via le script unifié `deploy.sh` (qui gère l'environnement virtuel Python) et `setup_searxng.sh` (qui gère l'orchestration Docker).
