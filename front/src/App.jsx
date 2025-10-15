import { useState } from 'react'
import Home from './pages/Home'
import GamePage from './pages/GamePage'
import './App.css'

function App() {
  const handleGameStart = (gameData) => {
    console.log('Démarrage de la partie:', gameData);
    // Ici tu pourras plus tard appeler ton API Django
    // et naviguer vers la page de jeu
  }

  return (
    //<Home onGameStart={handleGameStart} />
    <GamePage />
  )
}

export default App
