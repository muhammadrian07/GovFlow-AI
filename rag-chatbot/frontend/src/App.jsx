import React, { useState, useEffect } from 'react'
import Login from './pages/Login'
import Signup from './pages/Signup'
import Chat from './pages/Chat'
import './App.css'

/**
 * Main App component
 * Handles routing between Login, Signup, and Chat pages
 * Manages persistent user authentication with localStorage
 */
function App() {
  const [currentPage, setCurrentPage] = useState('login')
  const [user, setUser] = useState(null)

  // Initialize from localStorage on mount
  useEffect(() => {
    const savedUser = localStorage.getItem('currentUser')
    if (savedUser) {
      try {
        setUser(JSON.parse(savedUser))
        setCurrentPage('chat')
      } catch (error) {
        console.error('Error parsing saved user:', error)
        localStorage.removeItem('currentUser')
      }
    }
  }, [])

  const handleLogin = (userData) => {
    setUser(userData)
    // Save to localStorage for persistence
    localStorage.setItem('currentUser', JSON.stringify(userData))
    setCurrentPage('chat')
  }

  const handleSignup = (formData) => {
    // Get existing users from localStorage
    const existingUsers = JSON.parse(localStorage.getItem('users') || '[]')
    
    // Check if user already exists
    const userExists = existingUsers.some(u => u.email === formData.email)
    if (userExists) {
      return { error: 'Email already registered' }
    }

    // Save new user account
    const newUser = {
      name: formData.name,
      email: formData.email,
      password: formData.password // In production, hash this!
    }
    existingUsers.push(newUser)
    localStorage.setItem('users', JSON.stringify(existingUsers))

    // Auto-login after signup
    const loginUser = {
      name: formData.name,
      email: formData.email
    }
    setUser(loginUser)
    localStorage.setItem('currentUser', JSON.stringify(loginUser))
    setCurrentPage('chat')
  }

  const handleLogout = () => {
    setUser(null)
    localStorage.removeItem('currentUser')
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
          <Login onLogin={handleLogin} onGoToSignup={handleGoToSignup} />
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
