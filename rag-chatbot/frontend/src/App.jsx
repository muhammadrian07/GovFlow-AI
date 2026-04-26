import React, { useState } from 'react'
import Login from './pages/Login'
import Signup from './pages/Signup'
import Chat from './pages/Chat'
import './App.css'

/**
 * Main App component
 * Handles routing between Login, Signup, and Chat pages
 */
function App() {
  const [currentPage, setCurrentPage] = useState('login')
  const [user, setUser] = useState(null)

  const handleLogin = (userData) => {
    setUser(userData)
    setCurrentPage('chat')
  }

  const handleSignup = (formData) => {
    setUser({
      name: formData.name,
      email: formData.email
    })
    setCurrentPage('chat')
  }

  const handleLogout = () => {
    setUser(null)
    setCurrentPage('login')
  }

  const handleGoToSignup = () => {
    setCurrentPage('signup')
  }

  const handleGoToLogin = () => {
    setCurrentPage('login')
  }

  return (
    <div className="app">
      {currentPage === 'login' && (
        <div onClick={() => handleGoToSignup()}>
          <Login onLogin={handleLogin} />
        </div>
      )}

      {currentPage === 'signup' && (
        <Signup 
          onSignup={handleSignup}
          onLogin={() => handleGoToLogin()}
        />
      )}

      {currentPage === 'chat' && user && (
        <Chat user={user} onLogout={handleLogout} />
      )}
    </div>
  )
}

export default App
