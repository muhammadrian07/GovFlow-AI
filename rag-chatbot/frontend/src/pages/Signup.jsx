import React, { useState } from 'react'
import './Signup.css'

/**
 * Signup component
 * Creates new user accounts and stores them in localStorage
 */
const Signup = ({ onSignup, onLogin }) => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: ''
  })
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    setError('')
    setSuccess('')

    // Validation
    if (!formData.name || !formData.email || !formData.password) {
      setError('Please fill in all fields')
      return
    }

    if (!formData.email.includes('@')) {
      setError('Please enter a valid email')
      return
    }

    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match')
      return
    }

    if (formData.password.length < 6) {
      setError('Password must be at least 6 characters')
      return
    }

    // Check for duplicate email
    const existingUsers = JSON.parse(localStorage.getItem('users') || '[]')
    const userExists = existingUsers.some(u => u.email === formData.email)
    
    if (userExists) {
      setError('Email already registered. Please sign in instead.')
      setTimeout(() => onLogin(), 2000)
      return
    }

    // Success
    setSuccess('Account created successfully! Redirecting...')
    setTimeout(() => {
      onSignup(formData)
    }, 1500)
  }

  return (
    <div className="signup-container">
      <div className="signup-card">
        <h1>Create Account</h1>
        <p className="subtitle">Join RAG Chatbot</p>

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="name">Full Name</label>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleChange}
              placeholder="John Doe"
            />
          </div>

          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              placeholder="your@email.com"
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              placeholder="••••••••"
            />
          </div>

          <div className="form-group">
            <label htmlFor="confirmPassword">Confirm Password</label>
            <input
              type="password"
              id="confirmPassword"
              name="confirmPassword"
              value={formData.confirmPassword}
              onChange={handleChange}
              placeholder="••••••••"
            />
          </div>

          {error && <div className="error-message">{error}</div>}
          {success && <div className="success-message">{success}</div>}

          <button type="submit" className="btn-signup">
            Sign Up
          </button>
        </form>

        <p className="login-link">
          Already have an account?{' '}
          <a href="#login" onClick={(e) => { e.preventDefault(); onLogin() }}>Sign in here</a>
        </p>
      </div>
    </div>
  )
}

export default Signup
