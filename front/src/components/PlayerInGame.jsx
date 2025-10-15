function PlayerInGame({ player }) {
  const getStatus = () => {
    if (player.has_busted) return 'Éliminé';
    if (player.has_stayed) return 'Stand';
    return 'Roll';
  };

  return (
    <div className={`player-row ${player.is_current ? 'current-player' : ''}`}>
      <span className="player-name">{player.name}</span>
      <span className="player-score">{player.score}</span>
      <span className="player-status">{getStatus()}</span>
    </div>
  );
}

export default PlayerInGame;
