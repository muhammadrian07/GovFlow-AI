import React, { useState, useRef, useEffect } from 'react'
import api from '../services/api'
import Message from './Message'
import './ChatBox.css'

/**
 * ChatBox component
 * Main chat interface with message history and input
 * 
 * @param {string} country - Selected country filter
 */
const ChatBox = ({ country }) => {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const messagesEndRef = useRef(null)

  // Auto-scroll to bottom when new messages arrive
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSendMessage = async (e) => {
    e.preventDefault()

    if (!input.trim()) return

    // Add user message to chat
    const userMessage = {
      sender: 'user',
      content: input,
      timestamp: new Date().toISOString()
    }

    setMessages(prev => [...prev, userMessage])
    setInput('')
    setLoading(true)

    try {
      // Call backend API
      const response = await api.post('/chat', {
        query: input,
        country: country,
        top_k: 5
      })

      // Add assistant message with sources
      const assistantMessage = {
        sender: 'assistant',
        content: response.data.answer,
        sources: response.data.sources,
        timestamp: new Date().toISOString()
      }

      setMessages(prev => [...prev, assistantMessage])
    } catch (error) {
      console.error('Error sending message:', error)

      // Add error message
      const errorMessage = {
        sender: 'assistant',
        content: `Sorry, I encountered an error: ${error.response?.data?.detail || error.message}. Please try again.`,
        timestamp: new Date().toISOString()
      }

      setMessages(prev => [...prev, errorMessage])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="chatbox">
      <div className="messages-container">
        {messages.length === 0 && (
          <div className="empty-state">
            <div className="empty-icon">💬</div>
            <h3>Welcome to RAG Chatbot</h3>
            <p>Ask any questions about government policies for {country}</p>
            <p className="empty-hint">Type your question below to get started</p>
          </div>
        )}

        {messages.map((msg, idx) => (
          <Message key={idx} message={msg} />
        ))}

        {loading && (
          <div className="loading-message">
            <div className="spinner"></div>
            <span>Thinking...</span>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      <form className="input-form" onSubmit={handleSendMessage}>
        <input
          type="text"
          placeholder={`Ask about ${country} policies...`}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          disabled={loading}
          className="input-field"
        />
        <button
          type="submit"
          disabled={loading || !input.trim()}
          className="send-button"
        >
          {loading ? '⏳' : '📤 Send'}
        </button>
      </form>
    </div>
  )
}

export default ChatBox
