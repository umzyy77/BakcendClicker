# 🎮 Hacking Clicker - Backend Documentation

## 📌 Introduction
Hacking Clicker est un jeu de type clicker où le joueur incarne un hacker qui commence avec un simple PC et doit accumuler de la puissance de hacking pour pirater des cibles de plus en plus complexes. Ce projet est divisé en un backend (Flask) et un frontend (Flutter). Ce document détaille le backend, ses fonctionnalités et son intégration avec le frontend.

---

## 🚀 Installation et Lancement

### 🛠️ Prérequis
- Python 3.x
- Un compte MySQL hébergé sur Aiven (ou une base MySQL compatible)
- Pip et virtualenv (optionnel mais recommandé)

### 📦 Installation

1. Créez un environnement virtuel et activez-le (optionnel mais recommandé) :
   ```bash
   python -m venv venv
   source venv/bin/activate  # Sur Linux/macOS
   venv\Scripts\activate  # Sur Windows
   ```

2. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

3. Configurez votre base de données MySQL sur Aiven en renseignant le fichier `.env` :
   ```env
   DB_HOST=nom_du_serveur.aivencloud.com
   DB_PORT=3306
   DB_USER=nom_utilisateur
   DB_PASSWORD=mot_de_passe
   DB_NAME=nom_de_la_base
   ```

4. Exécutez le script pour initialiser la base de données :
   ```bash
   python utils/execute_sql.py
   ```

5. Lancez le backend :
   ```bash
   python app.py
   ```

6. (Optionnel) Pour réinitialiser la base de données :
   ```bash
   python utils/reset_db.py
   ```

7. (Optionnel) Pour afficher le contenu de la base de données :
   ```bash
   python utils/show_database.py
   ```

---

---

## 📌 API Endpoints

### 📌 Joueurs (/players)
- **Créer un joueur** → `POST /players`
- **Récupérer un joueur** → `GET /players/<player_id>`
- **Supprimer un joueur** → `DELETE /players/<player_id>`
- **Mettre à jour l'argent** → `PATCH /players/<player_id>/money`
- **Mettre à jour la puissance de hacking** → `PATCH /players/<player_id>/hacking_power`

### 📌 Missions (/missions)
- **Récupérer une mission** → `GET /missions/<mission_id>`
- **Lister toutes les missions** → `GET /missions`
- **Récupérer l'objectif d'une mission** → `GET /missions/<mission_id>/objective`

### 📌 Missions Joueur (/player_missions)
- **Récupérer les missions d'un joueur** → `GET /player_missions/<player_id>`
- **Démarrer une mission** → `POST /player_missions/<player_id>/start`
- **Incrémenter les clics** → `PATCH /player_missions/<player_id>/increment`
- **Vérifier une nouvelle mission débloquée** → `GET /player_missions/<player_id>/newly_unlocked`

### 📌 Améliorations (/upgrades)
- **Récupérer le bonus total de clics** → `GET /upgrades/<player_id>/total_click_bonus`
- **Voir toutes les améliorations** → `GET /upgrades/<player_id>`
- **Acheter une amélioration** → `POST /upgrades/<player_id>/buy`

---

## 🎮 Mécanique de Jeu & Gameloop

### 🔄 Gameloop du Clicker Game
La gameloop est la mécanique centrale du jeu et repose sur l'incrémentation des clics pour remplir des missions.

#### 📌 Fonctionnement de la Gameloop
1. **Lancement du jeu**
   - Vérification si un joueur existe, sinon création d’un nouveau joueur.
   - Assignation des missions de base.

2. **Démarrage d’une mission**
   - Le joueur sélectionne une mission parmi celles débloquées.
   - La mission passe en statut `in_progress`.

3. **Clics et progression**
   - Chaque clic envoie une requête `PATCH /player_missions/<player_id>/increment`.
   - L’API met à jour le compteur `clicks_done` et vérifie si l'objectif `clicks_required` est atteint.
   - Le total de clics pris en compte inclut les améliorations achetées (`UpgradeService.get_total_click_bonus`).

4. **Validation d’une mission**
   - Si les `clicks_done` atteignent ou dépassent `clicks_required`, la mission passe en statut `completed`.
   - Le joueur reçoit sa récompense en argent et en puissance de hacking.
   - La mission suivante est débloquée (`assign_next_mission`).

5. **Prochaine mission**
   - Le joueur peut choisir de démarrer une nouvelle mission débloquée ou améliorer ses capacités via la boutique.
   
---

## 📌 Services du Backend
### 🎮 Player Mission Service (player_mission_service.py)
- **Créer les missions d’un joueur** (`assign_default_missions`)
- **Démarrer une mission** (`start_mission`)
- **Récupérer les missions du joueur** (`get_missions_for_player`)
- **Vérifier une nouvelle mission débloquée** (`check_newly_unlocked_mission`)
- **Incrémenter les clics** (`increment_clicks` - Gameloop principale)
- **Compléter une mission** (`complete_mission`)
- **Débloquer la mission suivante** (`assign_next_mission`)

### 🏆 Mission Service (mission_service.py)
- **Récupérer une mission** (`get_mission`)
- **Lister toutes les missions** (`get_all_missions`)
- **Récupérer l’objectif d’une mission** (`get_mission_objective`)

### 🎯 Player Mission Service (player_mission_service.py)
- **Créer les missions d’un joueur** (`assign_default_missions`)
- **Démarrer une mission** (`start_mission`)
- **Incrémenter les clics** (`increment_clicks` - Gameloop principale)
- **Compléter une mission** (`complete_mission`)
- **Débloquer la mission suivante** (`assign_next_mission`)

### 💡 Upgrade Service (upgrade_service.py)
- **Récupérer le total de clics bonus** (`get_total_click_bonus`)
- **Lister toutes les améliorations** (`get_all_upgrades`)
- **Acheter une amélioration** (`buy_upgrade`)

---

## 📌 Conclusion
Le backend de **Hacking Clicker** permet une gestion complète du jeu avec un système de missions, améliorations et progression du joueur. Il est conçu pour être extensible et évolutif. 🚀