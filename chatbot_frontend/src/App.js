import React, { useState } from "react";
import Chatbot from "./Chatbot";
import "./App.css";

function App() {
  const [isChatOpen, setIsChatOpen] = useState(false);

  const toggleChat = () => {
    setIsChatOpen((prev) => !prev);
  };

  return (
    <div className="App">
      {/* Chat Button */}
      <div className="chat-widget">
        <div className="chat-button" onClick={toggleChat}>
          {isChatOpen ? "✕" : "💬"}
        </div>

        {/* Chatbot Container */}
        {isChatOpen && <Chatbot />}
      </div>
    </div>
  );
}

export default App;
