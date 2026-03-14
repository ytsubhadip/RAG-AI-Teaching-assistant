import { useState, useEffect, useRef } from "react"
import ReactMarkdown from "react-markdown"
import "./index.css"

function App() {

  const [message, setmessage] = useState("")
  const [messages, setmessages] = useState([])
  const [isTyping, setIsTyping] = useState(false)
  const chatEndRef = useRef(null)

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages, isTyping])

  const sendMessage = async () => {

    if (!message) return

    // add user message to UI
    setmessages([...messages, { sender: "user", text: message }])

    setIsTyping(true)

    // send request to FastAPI
    const res = await fetch("http://127.0.0.1:8000/getchat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        message: message
      })
    })

    const data = await res.json()

    setIsTyping(false)

    // show bot reply
    setmessages(prev => [
      ...prev,
      { sender: "bot", text: data["llm responce"] }
    ])

    setmessage("")
  }

  return (
    <div className="container">
      <header>
        <h1>AI Python Mentor</h1>
        <p>Power by Code With Harry</p>
      </header>

      {/* chat message area  */}
      <div className="chat-box">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.sender}`}>
            <b>{msg.sender === "bot" ? "AI ASSISTANT" : "YOU"}</b>
            {msg.sender === "bot" ? (
              <ReactMarkdown>{msg.text}</ReactMarkdown>
            ) : (
              <p>{msg.text}</p>
            )}
          </div>
        ))}

        {isTyping && (
          <div className="message bot typing">
            <div className="typing-dots">
              <div className="typing-dot"></div>
              <div className="typing-dot"></div>
              <div className="typing-dot"></div>
            </div>
            <span>AI is thinking...</span>
          </div>
        )}
        <div ref={chatEndRef} />
      </div>

      {/* input message section  */}
      <div className="input-area">
        <div className="input-box">
          <input
            type="text"
            value={message}
            onChange={(e) => setmessage(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
            placeholder="Ask anything about Python..."
          />
          <button onClick={sendMessage} aria-label="Send message">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
              <line x1="22" y1="2" x2="11" y2="13"></line>
              <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
            </svg>
          </button>
        </div>
      </div>
    </div>
  )
}

export default App