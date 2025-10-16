import { useState } from "react";

export const useStartGame = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [gameId, setGameId] = useState(null);

  const startGame = async (gameName, players) => {
    setLoading(true);
    setError(null);
    
    try {
      // Appel API pour créer la partie
      const response = await fetch('http://localhost:8000/api/games/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name: gameName,
          players: players.map(name => ({ name }))
        })
      });

      if (!response.ok) {
        throw new Error('Erreur lors de la création de la partie');
      }

      const data = await response.json();
      setGameId(data.id);
      return data;
      
    } catch (err) {
      setError(err.message);
      console.error('Erreur:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return { startGame, loading, error, gameId };
};
