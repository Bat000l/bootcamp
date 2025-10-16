import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { useGameState } from '../hooks/useGameState';
import PlayerInGame from '../components/PlayerInGame';
import '../styles/GamePage.css';

function GamePage() {
  const { gameId } = useParams();
  const [diceCount, setDiceCount] = useState(1);
  const { game, loading, error, rollDice, stand } = useGameState(gameId);

  if (loading) {
    return <div>Chargement...</div>;
  }

  if (error) {
    return <div className="error-message">{error}</div>;
  }

  if (!game) {
    return <div>Erreur lors du chargement de la partie</div>;
  }

  const currentPlayer = game.players.find(p => p.is_current);

  return (
    <div className="game-container">
      <div className="game-card">
        <h1>{game.name}</h1>
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
          <button className="btn-action" onClick={() => rollDice(diceCount)} disabled={loading}>
            ROLL
          </button>
          <button className="btn-action btn-secondary" onClick={stand} disabled={loading}>
            STAND
          </button>
        </div>
        <div className="players-section">
          <h2>Joueurs</h2>
          <div className="players-list">
            {game.players && game.players.map((player) => (
              <PlayerInGame key={player.id} player={player} />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default GamePage;
