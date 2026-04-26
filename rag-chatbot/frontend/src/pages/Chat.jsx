import React, { useState } from 'react'
import ChatBox from '../components/ChatBox'
import Filter from '../components/Filter'
import './Chat.css'

/**
 * Main Chat page component
 * Displays chat interface with country filter
 */
const Chat = ({ user, onLogout }) => {
  const [selectedCountry, setSelectedCountry] = useState('USA')

  return (
    <div className="chat-container">
      <header className="chat-header">
        <div className="header-left">
          <h1>📚 Government Policy Assistant</h1>
          <p>Powered by RAG</p>
        </div>
        <div className="header-right">
          <span className="user-name">👤 {user.name}</span>
          <button onClick={onLogout} className="btn-logout">
            Logout
          </button>
        </div>
      </header>

      <main className="chat-main">
        <div className="chat-wrapper">
          <Filter 
            selectedCountry={selectedCountry}
            onCountryChange={setSelectedCountry}
          />
          <ChatBox country={selectedCountry} />
        </div>
      </main>

      <footer className="chat-footer">
        <p>© 2024 RAG Chatbot. All rights reserved.</p>
      </footer>
    </div>
  )
}

export default Chat
