import { useState, useEffect, useCallback } from 'react';

export function useGameState(gameId) {
  const [game, setGame] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Charge l'état de la partie
  const fetchGame = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`http://localhost:8000/game/${gameId}`);
      if (!res.ok) throw new Error('Impossible de charger la partie');
      const data = await res.json();
      setGame(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [gameId]);

  useEffect(() => {
    if (gameId) fetchGame();
  }, [gameId, fetchGame]);

  // Action: roll
  const rollDice = useCallback(async (diceCount) => {
    setError(null);
    try {
      const res = await fetch(`http://localhost:8000/game/play`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ game_id: Number(gameId), action: 'roll', num_dice: diceCount })
      });
      if (!res.ok) throw new Error('Erreur lors du roll');
      const data = await res.json();
      if (data.success && data.game) {
        setGame(data.game);
      } else {
        throw new Error(data.message || 'Erreur lors du roll');
      }
    } catch (err) {
      setError(err.message);
    }
  }, [gameId]);

  // Action: stand
  const stand = useCallback(async () => {
    setError(null);
    try {
      const res = await fetch(`http://localhost:8000/game/play`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ game_id: Number(gameId), action: 'stand' })
      });
      if (!res.ok) throw new Error('Erreur lors du stand');
      const data = await res.json();
      if (data.success && data.game) {
        setGame(data.game);
      } else {
        throw new Error(data.message || 'Erreur lors du stand');
      }
    } catch (err) {
      setError(err.message);
    }
  }, [gameId]);

  return { game, loading, error, rollDice, stand, fetchGame };
}
