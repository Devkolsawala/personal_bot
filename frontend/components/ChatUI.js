import { useState } from "react";
import axios from "axios";

export default function ChatUI() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const newMessage = { sender: "user", text: input };
    setMessages([...messages, newMessage]);
    setInput("");
    setLoading(true);

    try {
      const res = await axios.post("http://127.0.0.1:8000/query", { query: input });


      const botMessage = { sender: "bot", text: res.data.response };
      setMessages([...messages, newMessage, botMessage]);
    } catch (error) {
      setMessages([
        ...messages,
        newMessage,
        { sender: "bot", text: "Error fetching response." },
      ]);
    }
    setLoading(false);
  };

  return (
    <div style={{ maxWidth: "600px", margin: "auto", paddingTop: "50px" }}>
      <h1>📚 Personal Document Chatbot</h1>
      <div
        style={{
          border: "1px solid #ccc",
          padding: "15px",
          borderRadius: "8px",
          height: "400px",
          overflowY: "auto",
        }}
      >
        {messages.map((msg, i) => (
          <p key={i} style={{ textAlign: msg.sender === "user" ? "right" : "left" }}>
            <strong>{msg.sender === "user" ? "You: " : "Bot: "}</strong>
            {msg.text}
          </p>
        ))}
        {loading && <p><em>Thinking...</em></p>}
      </div>
      <div style={{ display: "flex", marginTop: "10px" }}>
        <input
          type="text"
          value={input}
          placeholder="Ask a question..."
          onChange={(e) => setInput(e.target.value)}
          style={{ flex: 1, padding: "10px" }}
        />
        <button onClick={sendMessage} style={{ padding: "10px 15px", marginLeft: "5px" }}>
          Send
        </button>
      </div>
    </div>
  );
}
