from django.test import TestCase, Client
from django.urls import reverse
import json
from blackjack.models import Game, Player

# Create your tests here.

class GameWinnersTestCase(TestCase):
    def setUp(self):
        """Create a game for testing"""
        self.game = Game.objects.create(name="Test Game", turn=0, ended=False)
    
    def test_winners_with_exact_21(self):
        """Test winners when one or more players have exactly 21"""
        # Create players with different scores
        player1 = Player.objects.create(name="Alice", score=21, game=self.game)
        player2 = Player.objects.create(name="Bob", score=19, game=self.game)
        player3 = Player.objects.create(name="Charlie", score=21, game=self.game)
        
        winners = self.game.winners()
        
        # Should return only players with 21
        self.assertEqual(len(winners), 2)
        self.assertIn(player1, winners)
        self.assertIn(player3, winners)
        self.assertNotIn(player2, winners)
    
    def test_winners_under_21(self):
        """Test winners when no player has 21, return highest under 21"""
        # Create players with scores under 21
        player1 = Player.objects.create(name="Alice", score=18, game=self.game)
        player2 = Player.objects.create(name="Bob", score=20, game=self.game)
        player3 = Player.objects.create(name="Charlie", score=20, game=self.game)
        
        winners = self.game.winners()
        
        # Should return players with highest score (20)
        self.assertEqual(len(winners), 2)
        self.assertIn(player2, winners)
        self.assertIn(player3, winners)
        self.assertNotIn(player1, winners)
    
    def test_winners_all_over_21(self):
        """Test winners when all players are over 21"""
        # Create players all over 21
        Player.objects.create(name="Alice", score=22, game=self.game)
        Player.objects.create(name="Bob", score=25, game=self.game)
        Player.objects.create(name="Charlie", score=23, game=self.game)
        
        winners = self.game.winners()
        
        # Should return empty list
        self.assertEqual(len(winners), 0)
    
    def test_winners_no_players(self):
        """Test winners when there are no players"""
        winners = self.game.winners()
        
        # Should return empty list
        self.assertEqual(len(winners), 0)
    
    def test_winners_single_player_at_21(self):
        """Test with a single player at 21"""
        player1 = Player.objects.create(name="Alice", score=21, game=self.game)
        
        winners = self.game.winners()
        
        self.assertEqual(len(winners), 1)
        self.assertEqual(winners[0], player1)


class GameCurrentPlayerTestCase(TestCase):
    def setUp(self):
        """Create a game for testing"""
        self.game = Game.objects.create(name="Test Game", turn=0, ended=False)
    
    def test_current_player_first_active(self):
        """Test current_player returns the first player who hasn't stood and is under 21"""
        # Create players with different states
        player1 = Player.objects.create(name="Alice", score=15, stand=False, game=self.game)
        player2 = Player.objects.create(name="Bob", score=18, stand=False, game=self.game)
        player3 = Player.objects.create(name="Charlie", score=20, stand=True, game=self.game)
        
        current = self.game.current_player()
        
        # Should return the first player who hasn't stood and is under 21
        self.assertEqual(current, player1)
    
    def test_current_player_skips_stood(self):
        """Test current_player skips players who have stood"""
        # First player has stood
        player1 = Player.objects.create(name="Alice", score=15, stand=True, game=self.game)
        player2 = Player.objects.create(name="Bob", score=18, stand=False, game=self.game)
        player3 = Player.objects.create(name="Charlie", score=10, stand=False, game=self.game)
        
        current = self.game.current_player()
        
        # Should skip Alice and return Bob (first non-stood player)
        self.assertEqual(current, player2)
    
    def test_current_player_skips_over_21(self):
        """Test current_player skips players with score >= 21"""
        # Create players
        player1 = Player.objects.create(name="Alice", score=21, stand=False, game=self.game)
        player2 = Player.objects.create(name="Bob", score=22, stand=False, game=self.game)
        player3 = Player.objects.create(name="Charlie", score=15, stand=False, game=self.game)
        
        current = self.game.current_player()
        
        # Should skip players with score >= 21 and return Charlie
        self.assertEqual(current, player3)
    
    def test_current_player_all_stood(self):
        """Test current_player returns None when all players have stood"""
        # All players have stood
        Player.objects.create(name="Alice", score=15, stand=True, game=self.game)
        Player.objects.create(name="Bob", score=18, stand=True, game=self.game)
        
        current = self.game.current_player()
        
        # Should return None
        self.assertIsNone(current)
    
    def test_current_player_all_over_21(self):
        """Test current_player returns None when all players are >= 21"""
        # All players are at or over 21
        Player.objects.create(name="Alice", score=21, stand=False, game=self.game)
        Player.objects.create(name="Bob", score=23, stand=False, game=self.game)
        
        current = self.game.current_player()
        
        # Should return None
        self.assertIsNone(current)
    
    def test_current_player_no_players(self):
        """Test current_player returns None when there are no players"""
        current = self.game.current_player()
        
        # Should return None
        self.assertIsNone(current)
    
    def test_current_player_mixed_states(self):
        """Test current_player with a mix of stood, over 21, and active players"""
        # Mix of states
        player1 = Player.objects.create(name="Alice", score=22, stand=False, game=self.game)  # Over 21
        player2 = Player.objects.create(name="Bob", score=18, stand=True, game=self.game)     # Stood
        player3 = Player.objects.create(name="Charlie", score=21, stand=False, game=self.game) # At 21
        player4 = Player.objects.create(name="David", score=16, stand=False, game=self.game)  # Active
        
        current = self.game.current_player()
        
        # Should return David (first active player under 21)
        self.assertEqual(current, player4)


class GameApiTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_start_game_api(self):
        response = self.client.post('/game/start', data=json.dumps({
            "name": "API Test Game",
            "players": ["Alice", "Bob"]
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['name'], "API Test Game")
        self.assertEqual(len(data['players']), 2)

    def test_play_roll_api(self):
        # Crée une partie
        start_resp = self.client.post('/game/start', data=json.dumps({
            "name": "API Test Game",
            "players": ["Alice", "Bob"]
        }), content_type='application/json')
        game_id = start_resp.json()['id']
        # Action roll
        play_resp = self.client.post('/game/play', data=json.dumps({
            "game_id": game_id,
            "action": "roll",
            "num_dice": 2
        }), content_type='application/json')
        self.assertEqual(play_resp.status_code, 200)
        play_data = play_resp.json()
        self.assertTrue(play_data['success'])
        self.assertIn('game', play_data)

    def test_play_stand_api(self):
        # Crée une partie
        start_resp = self.client.post('/game/start', data=json.dumps({
            "name": "API Test Game",
            "players": ["Alice", "Bob"]
        }), content_type='application/json')
        game_id = start_resp.json()['id']
        # Action stand
        play_resp = self.client.post('/game/play', data=json.dumps({
            "game_id": game_id,
            "action": "stand"
        }), content_type='application/json')
        self.assertEqual(play_resp.status_code, 200)
        play_data = play_resp.json()
        self.assertTrue(play_data['success'])
        self.assertIn('game', play_data)

    def test_get_game_api(self):
        # Crée une partie
        start_resp = self.client.post('/game/start', data=json.dumps({
            "name": "API Test Game",
            "players": ["Alice", "Bob"]
        }), content_type='application/json')
        game_id = start_resp.json()['id']
        # GET état
        get_resp = self.client.get(f'/game/{game_id}')
        self.assertEqual(get_resp.status_code, 200)
        get_data = get_resp.json()
        self.assertEqual(get_data['id'], game_id)
        self.assertEqual(get_data['name'], "API Test Game")
