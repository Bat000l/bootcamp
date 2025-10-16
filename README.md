# Blackjack Game – Django & React (Dockerized)

## Présentation

Ce projet est un jeu de Blackjack développé avec Django (backend API) et React (frontend). Il est entièrement dockerisé pour une utilisation et un déploiement ultra-simples. Idéal pour découvrir le développement fullstack moderne, l'intégration API, et la conteneurisation.

---

## Fonctionnalités

- **Backend Django** :
  - API REST pour gérer les parties, joueurs, actions (tirer, rester).
  - Utilisation de Django Ninja pour la rapidité et la simplicité.
  - Modélisation des parties et joueurs.
  - Tests unitaires pour la logique et les endpoints.
- **Frontend React** :
  - Interface utilisateur moderne (Vite + React).
  - Affichage dynamique de l’état du jeu, du joueur courant, du gagnant.
  - Hooks personnalisés pour la gestion du state et des appels API.
  - Tests unitaires pour les hooks et composants clés.
- **Docker** :
  - Conteneurs séparés pour le backend et le frontend.
  - Configuration docker-compose pour tout lancer en une commande.
  - Prêt pour le déploiement local ou cloud.

---

## Prérequis

- [Docker Desktop](https://www.docker.com/products/docker-desktop) (Windows, Mac, Linux)
- (Optionnel) [Git](https://git-scm.com/) pour cloner le projet

---

## Installation rapide

1. **Cloner le projet**
   ```bash
   git clone https://github.com/Bat000l/bootcamp.git
   cd bootcamp
   ```
2. **Lancer les conteneurs Docker**
   ```bash
   docker-compose up --build
   ```
   - Le backend démarre sur [http://localhost:8000](http://localhost:8000)
   - Le frontend démarre sur [http://localhost:5173](http://localhost:5173)

---

## Utilisation

- **Accéder au jeu** : Ouvrez [http://localhost:5173](http://localhost:5173) dans votre navigateur.
- **API endpoints principaux** :
  - `POST /api/start` : Démarre une nouvelle partie
  - `POST /api/play` : Effectue une action (tirer, rester)
  - `GET /api/game/{id}` : Récupère l’état d’une partie
- **Tests** :
  - Backend :
    ```bash
    docker-compose exec backend python manage.py test blackjack
    ```
  - Frontend :
    ```bash
    docker-compose exec front npm test
    ```

---

## Structure du projet

```
bootcamp/
├── blackjack/           # App Django principale
│   ├── models.py        # Modèles de données
│   ├── services.py      # Logique métier
│   ├── views.py         # Endpoints API
│   ├── tests.py         # Tests unitaires backend
│   └── ...
├── bootcamp/            # Config Django
│   └── ...
├── front/               # Frontend React
│   ├── src/
│   │   ├── hooks/       # Hooks personnalisés
│   │   ├── components/  # Composants UI
│   │   └── ...
│   ├── Dockerfile       # Build frontend
│   ├── package.json     # Dépendances React
│   └── ...
├── docker-compose.yml   # Orchestration Docker
├── requirements.txt     # Dépendances Python
├── README.md            # Ce fichier
└── ...
```

---

## Configuration Docker

- **Backend** : Python 3.11, Django, django-ninja, django-cors-headers
- **Frontend** : Node 20, Vite, React
- **Volumes** :
  - Persistance du code et des dépendances
  - Exclusion de `node_modules` pour éviter les bugs Rollup
- **Ports exposés** :
  - Backend : 8000
  - Frontend : 5173

---

## Développement local (hors Docker)

1. **Backend** :
   - Créer un venv : `python -m venv venv`
   - Activer : `venv\Scripts\activate` (Windows) ou `source venv/bin/activate` (Linux/Mac)
   - Installer : `pip install -r requirements.txt`
   - Lancer : `python manage.py runserver`
2. **Frontend** :
   - Installer Node.js (>= 20)
   - Installer les dépendances : `npm install`
   - Lancer : `npm run dev`

---

## Tests

- **Backend** :
  - Fichier : `blackjack/tests.py`
  - Commande : `python manage.py test blackjack`
- **Frontend** :
  - Fichier : `front/src/hooks/__tests__/useGameState.test.js`
  - Commande : `npm test`

---

## Déploiement

- Le projet est prêt pour un déploiement sur n’importe quel serveur Docker (cloud, VPS, etc).
- Adapter les variables d’environnement et la config de la base de données pour la production.

---

## Auteur

- Bat000l
- Contact : [GitHub](https://github.com/Bat000l)
  ```

  ```
- Pour arrêter :
  ```sh
  docker-compose down
  ```
