import React, { useState } from 'react'
import './Login.css'

/**
 * Login component
 * Mock authentication page (no backend verification)
 * In production, integrate with real auth service
 */
const Login = ({ onLogin }) => {
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

    // Mock authentication (no backend call)
    // In production, verify credentials with backend
    if (password.length < 6) {
      setError('Password must be at least 6 characters')
      return
    }

    // Success
    onLogin({ email, name: email.split('@')[0] })
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
          <a href="#signup">Sign up here</a>
        </p>
      </div>
    </div>
  )
}

export default Login
