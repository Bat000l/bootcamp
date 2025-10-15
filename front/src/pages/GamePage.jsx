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
  const [diceCount, setDiceCount] = useState(1);



  if (loading) {
    return <div>Chargement...</div>;
  }

  if (!gameState) {
    return <div>Erreur lors du chargement de la partie</div>;
  }

  const handleRoll = () => {
    console.log(`ROLL with ${diceCount} dice(s)`);
    // TODO: call backend roll endpoint with diceCount when ready
  };

  const currentPlayer = gameState.players.find(p => p.is_current);

  return (
    <div className="game-container">
      <div className="game-card">
        <h1>{gameState.name}</h1>
        <div className="current-turn">
          Au tour de "{currentPlayer?.name || 'Personne'}"
        </div>
        <div className="dice-controls">
          <label htmlFor="diceCount">Nombre de dés</label>
          <select
            id="diceCount"
            className="select-control"
            value={diceCount}
            onChange={(e) => setDiceCount(Number(e.target.value))}
          >
            {[1,2,3].map(n => (
              <option key={n} value={n}>{n}</option>
            ))}
          </select>
          <button className="btn-action" onClick={handleRoll}>ROLL</button>
          <button className="btn-action btn-secondary" onClick={() => console.log('STAND')}>STAND</button>
        </div>
        <div className="players-section">
          <h2>Joueurs</h2>
          <div className="players-list">
            {gameState.players && gameState.players.map((player) => (
              <PlayerInGame key={player.id} player={player} />
            ))}
          </div>
        </div>


      </div>
    </div>
  );
}

export default GamePage;
