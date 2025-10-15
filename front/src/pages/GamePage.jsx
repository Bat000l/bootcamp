import { useState, useEffect } from 'react';
import PlayerInGame from '../components/PlayerInGame';
import './GamePage.css';

function GamePage({ gameId }) {

  const [gameState, setGameState] = useState({
    name: "Partie de test",
    players: [
      { id: 1, name: "Alice", score: 18, has_busted: false, has_stayed: true, is_current: false },
      { id: 2, name: "Bob", score: 15, has_busted: false, has_stayed: false, is_current: true },
      { id: 3, name: "Charlie", score: 23, has_busted: true, has_stayed: false, is_current: false },
      { id: 4, name: "Diana", score: 12, has_busted: false, has_stayed: false, is_current: false }
    ]
  });
  const [loading, setLoading] = useState(false);



  if (loading) {
    return <div>Chargement...</div>;
  }

  if (!gameState) {
    return <div>Erreur lors du chargement de la partie</div>;
  }

  return (
    <div>
      <div>
        <h1>{gameState.name}</h1>
        
        <div>
          <h2>Joueurs</h2>
          <div>
            {gameState.players && gameState.players.map((player) => (
              <PlayerInGame key={player.id} player={player} />
            ))}
          </div>
        </div>

        <div>
          <button onClick={() => console.log('ROLL')}>
            ROLL
          </button>
          <button onClick={() => console.log('STAND')}>
            STAND
          </button>
        </div>
      </div>
    </div>
  );
}

export default GamePage;
