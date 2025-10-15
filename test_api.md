# Test de l'API Blackjack

## URLs disponibles

- **Documentation interactive** : http://localhost:8000/game/docs
- **Base de l'API** : http://localhost:8000/game/

## Endpoints

### 1. Démarrer une partie
```
POST http://localhost:8000/game/start
Content-Type: application/json

{
    "name": "Ma partie",
    "players": ["Alice", "Bob", "Charlie"]
}
```

### 2. Jouer un tour
```
POST http://localhost:8000/game/play
Content-Type: application/json

{
    "game_id": 1,
    "action": "hit"
}
```

OU

```
POST http://localhost:8000/game/play
Content-Type: application/json

{
    "game_id": 1,
    "action": "stand"
}
```

### 3. Récupérer l'état d'une partie
```
GET http://localhost:8000/game/1
```

## Test avec curl (PowerShell)

### Démarrer une partie
```powershell
curl -X POST http://localhost:8000/game/start -H "Content-Type: application/json" -d '{\"name\":\"Ma partie\",\"players\":[\"Alice\",\"Bob\",\"Charlie\"]}'
```

### Jouer (hit)
```powershell
curl -X POST http://localhost:8000/game/play -H "Content-Type: application/json" -d '{\"game_id\":1,\"action\":\"hit\"}'
```

### Jouer (stand)
```powershell
curl -X POST http://localhost:8000/game/play -H "Content-Type: application/json" -d '{\"game_id\":1,\"action\":\"stand\"}'
```

### Voir l'état de la partie
```powershell
curl http://localhost:8000/game/1
```

## Fonctionnement

1. **Démarrer une partie** : Créer une partie avec des joueurs
2. **Le premier joueur joue** : "hit" pour tirer une carte, "stand" pour s'arrêter
3. **Le tour passe automatiquement** au joueur suivant
4. **La partie se termine** quand tous les joueurs ont stand ou dépassé 21
5. **Les gagnants sont calculés** : joueur(s) avec le meilleur score ≤ 21
