from ninja import NinjaAPI, Schema
from typing import List, Optional
from blackjack.models import Game, Player
from blackjack.services import start_game
import random

api = NinjaAPI()

# Schemas pour les requêtes et réponses

class StartGameSchema(Schema):
    name: str
    players: List[str]

class PlayerSchema(Schema):
    id: int
    name: str
    score: int
    stand: bool

class GameSchema(Schema):
    id: int
    name: str
    turn: int
    ended: bool
    players: List[PlayerSchema]
    current_player: Optional[PlayerSchema] = None
    winners: List[PlayerSchema] = []

class PlayActionSchema(Schema):
    game_id: int
    action: str  # "roll" ou "stand"
    num_dice: Optional[int] = 1  # Nombre de dés (1, 2 ou 3)

class PlayResponseSchema(Schema):
    success: bool
    message: str
    game: GameSchema

# Endpoints

@api.post("/start", response=GameSchema)
def start(request, data: StartGameSchema):

    game = start_game(data.name, data.players)
    
    players_data = [
        PlayerSchema(
            id=p.id,
            name=p.name,
            score=p.score,
            stand=p.stand
        ) for p in game.players.all()
    ]
    
    current = game.current_player()
    current_data = PlayerSchema(
        id=current.id,
        name=current.name,
        score=current.score,
        stand=current.stand
    ) if current else None
    
    return GameSchema(
        id=game.id,
        name=game.name,
        turn=game.turn,
        ended=game.ended,
        players=players_data,
        current_player=current_data,
        winners=[]
    )

@api.post("/play", response=PlayResponseSchema)
def play(request, data: PlayActionSchema):
    """Permet au joueur actuel de jouer (roll ou stand)"""
    try:
        game = Game.objects.get(id=data.game_id)
    except Game.DoesNotExist:
        return PlayResponseSchema(
            success=False,
            message="Partie introuvable",
            game=None
        )
    
    if game.ended:
        return PlayResponseSchema(
            success=False,
            message="La partie est terminée",
            game=_build_game_schema(game)
        )
    
    player = game.current_player()
    
    if player is None:
        # Plus de joueurs actifs, terminer la partie
        game.ended = True
        game.save()
        return PlayResponseSchema(
            success=True,
            message="La partie est terminée, plus de joueurs actifs",
            game=_build_game_schema(game)
        )
    
    # Effectuer l'action
    if data.action == "roll":
        # Valider le nombre de dés
        num_dice = data.num_dice if data.num_dice else 1
        if num_dice < 1 or num_dice > 3:
            return PlayResponseSchema(
                success=False,
                message="Vous devez lancer entre 1 et 3 dés",
                game=_build_game_schema(game)
            )
        
        # Lancer les dés
        dice_results = [random.randint(1, 6) for _ in range(num_dice)]
        dice_sum = sum(dice_results)
        player.score += dice_sum
        player.save()
        
        dice_str = ", ".join(map(str, dice_results))
        message = f"{player.name} lance {num_dice} dé(s) : [{dice_str}] = {dice_sum}. Score total: {player.score}"
        
        # Si le joueur atteint ou dépasse 21, il passe automatiquement en stand
        if player.score >= 21:
            player.stand = True
            player.save()
            if player.score == 21:
                message += " - Blackjack!"
            else:
                message += " - Dépassé!"

    elif data.action == "stand":
        # Le joueur décide de s'arrêter
        player.stand = True
        player.save()
        message = f"{player.name} décide de rester à {player.score}"
    
    else:
        return PlayResponseSchema(
            success=False,
            message=f"Action invalide: {data.action}. Utilisez 'roll' ou 'stand'",
            game=_build_game_schema(game)
        )
    
    # Incrémenter le tour
    game.turn += 1
    game.save()
    
    # Vérifier s'il reste des joueurs actifs
    if game.current_player() is None:
        game.ended = True
        game.save()
        message += " - Partie terminée!"
    
    return PlayResponseSchema(
        success=True,
        message=message,
        game=_build_game_schema(game)
    )

@api.get("/{pk}", response=GameSchema)
def get_game(request, pk: int):
    """Récupère l'état d'une partie"""
    try:
        game = Game.objects.get(id=pk)
    except Game.DoesNotExist:
        return {"error": "Partie introuvable"}
    
    return _build_game_schema(game)


def _build_game_schema(game: Game) -> GameSchema:
    players_data = [
        PlayerSchema(
            id=p.id,
            name=p.name,
            score=p.score,
            stand=p.stand
        ) for p in game.players.all()
    ]
    
    current = game.current_player()
    current_data = PlayerSchema(
        id=current.id,
        name=current.name,
        score=current.score,
        stand=current.stand
    ) if current else None
    
    winners = game.winners() if game.ended else []
    winners_data = [
        PlayerSchema(
            id=w.id,
            name=w.name,
            score=w.score,
            stand=w.stand
        ) for w in winners
    ]
    
    return GameSchema(
        id=game.id,
        name=game.name,
        turn=game.turn,
        ended=game.ended,
        players=players_data,
        current_player=current_data,
        winners=winners_data
    )