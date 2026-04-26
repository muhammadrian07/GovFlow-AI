import React from 'react'
import './Message.css'

/**
 * Message component
 * Displays individual messages in the chat
 * 
 * @param {Object} message - Message object with content, sender, timestamp
 */
const Message = ({ message }) => {
  const isUser = message.sender === 'user'

  return (
    <div className={`message-container ${isUser ? 'user' : 'assistant'}`}>
      <div className="message">
        <div className="message-content">
          {message.content}
        </div>
        <div className="message-time">
          {new Date(message.timestamp).toLocaleTimeString()}
        </div>

        {/* Show sources for assistant messages */}
        {!isUser && message.sources && message.sources.length > 0 && (
          <div className="message-sources">
            <strong>📚 Sources:</strong>
            <ul>
              {message.sources.map((source, idx) => (
                <li key={idx}>
                  <span className="source-file">{source.source}</span>
                  {source.page && <span className="source-page">p. {source.page}</span>}
                  <div className="source-text">{source.text}</div>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  )
}

export default Message
