from blackjack.models import Game, Player

def start_game(name, players: list[str]) -> Game:

    #create game
    game = Game.objects.create(name=name, turn=0, ended=False)

    #create players
    for player_name in players:
        Player.objects.create(name=player_name, game=game)


    #add players to game
    #save game
    game.save()
    #return game

    return game