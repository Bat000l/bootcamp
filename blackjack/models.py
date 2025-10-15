from django.db import models
from django.db.models import Sum, Avg, Max
# Create your models here.
class Game (models.Model):
    name = models.CharField(max_length=250)
    turn = models.IntegerField(default=0)
    ended = models.BooleanField(default=False)

    def winners(self):
        result = []
        players = self.players.all()
        # get winnners        
        #player == 21 if exists
        #player < 21 if no players at 21
        #can have multiple winners
        exact_winners = players.filter(score=21)
        under_winners = players.filter(score__lt=21)
        if exact_winners.exists():
            result = list(exact_winners)
            return result
        else:
            if under_winners.exists():
                max_score = under_winners.aggregate(Max('score'))['score__max']
                result = list(under_winners.filter(score=max_score))
                return result
        return []
    
    def current_player(self):
        # filterd_players = players.filtered 
        # by stand is False and player < 21 
        # get current in filtered_players
        filtered_players = self.players.filter(stand=False, score__lt=21)
        if filtered_players.exists():
            player_count = filtered_players.count()
            current_index = self.turn % player_count
            return filtered_players[current_index]
        return None

class Player (models.Model):
    name = models.CharField(max_length=250)
    score = models.IntegerField(default=0)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='players')
    stand = models.BooleanField(default=False)
