import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import PlayerInput from '../components/PlayerInput';
import { useStartGame } from '../hooks/useStartGame';
import '../styles/Home.css';

function Home() {
  const [gameName, setGameName] = useState('');
  const [players, setPlayers] = useState(['']);
  const { startGame, loading, error } = useStartGame();
  const navigate = useNavigate();

  const handlePlayerChange = (index, value) => {
    const updatedPlayers = [...players];
    updatedPlayers[index] = value;
    // Ajoute un nouvel input si le dernier est rempli
    if (index === players.length - 1 && value.trim() !== '') {
      updatedPlayers.push('');
    }
    setPlayers(updatedPlayers);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!gameName.trim()) {
      alert('Veuillez entrer un nom de partie');
      return;
    }
    const filteredPlayers = players.filter(name => name.trim() !== '');
    if (filteredPlayers.length === 0) {
      alert('Veuillez ajouter au moins un joueur');
      return;
    }
    
    try {
      const game = await startGame(gameName, filteredPlayers);
      navigate(`/game/${game.id}`);
    } catch (err) {
      // L'erreur est déjà affichée dans le hook
      console.error('Impossible de créer la partie');
    }
  };

  return (
    <div className="home-container">    
        <h1>Blackjack</h1>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <input
              type="text"
              value={gameName}
              onChange={e => setGameName(e.target.value)}
              className="input-field"
              placeholder="Nom de la partie"
            />
          </div>
          <div className="form-group">
            <label>Joueurs</label>
            {players.map((value, idx) => (
              <PlayerInput
                key={idx}
                value={value}
                onChange={handlePlayerChange}
                index={idx}
              />
            ))}
          </div>
          {error && <div className="error-message">{error}</div>}
          <button type="submit" className="btn-start" disabled={loading}>
            {loading ? 'Création...' : 'Lancer la partie'}
          </button>
        </form>
    </div>
  );
}

export default Home;
