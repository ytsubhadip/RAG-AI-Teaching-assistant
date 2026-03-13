import { useState } from "react"
import ReactMarkdown from "react-markdown"
import "./index.css"
function App() {

  const [message, setmessage] = useState("")
  const [messages, setmessages] = useState([])
  
  const sendMessage = async () => {

  if (!message) return

  // add user message to UI
  setmessages([...messages, { sender: "user", text: message }])

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

  // show bot reply
  setmessages(prev => [
    ...prev,
    { sender: "bot", text: data["llm responce"] }
  ])

  setmessage("")
}
  
  return (
    <div className="container">
      <h1>Learn Python Code With Harry</h1>

      {/* chat message area  */}
      <div className="chat-box">
        {/* <p><b>User</b> Hello</p>
          <p><b>CHW</b> wellcome to code with harry</p> */}

        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.sender}`}>
            <b>{msg.sender}:</b> {msg.sender === "bot" ? (
              <ReactMarkdown>{msg.text}</ReactMarkdown>
            ) : (
              msg.text
            )}
          </div>
        ))}
      </div>

      {/* input message section  */}

      <div className="input-box">
        <input
          type="text"
          value={message}
          onChange={(e) => setmessage(e.target.value)}
          placeholder="Type message..."
        />
        <button onClick={sendMessage} >Send</button>
      
      </div>
    </div>
  )
}

export default App