import React, { useState } from 'react'
import './Login.css'

/**
 * Login component
 * Validates credentials against users stored in localStorage
 */
const Login = ({ onLogin, onGoToSignup }) => {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    setError('')

    // Basic validation
    if (!email || !password) {
      setError('Please fill in all fields')
      return
    }

    if (!email.includes('@')) {
      setError('Please enter a valid email')
      return
    }

    if (password.length < 6) {
      setError('Password must be at least 6 characters')
      return
    }

    // Verify credentials against stored users
    const users = JSON.parse(localStorage.getItem('users') || '[]')
    const user = users.find(u => u.email === email)

    if (!user) {
      setError('Email not found. Please sign up first.')
      setTimeout(() => onGoToSignup(), 1500)
      return
    }

    if (user.password !== password) {
      setError('Incorrect password')
      return
    }

    // Success - login with found user
    onLogin({ email: user.email, name: user.name })
  }

  return (
    <div className="login-container">
      <div className="login-card">
        <h1>RAG Chatbot</h1>
        <p className="subtitle">Government Policy Assistant</p>

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="your@email.com"
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
            />
          </div>

          {error && <div className="error-message">{error}</div>}

          <button type="submit" className="btn-login">
            Sign In
          </button>
        </form>

        <p className="signup-link">
          Don't have an account?{' '}
          <a href="#signup" onClick={(e) => { e.preventDefault(); onGoToSignup() }}>Sign up here</a>
        </p>
      </div>
    </div>
  )
}

export default Login
