import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import './Chatbot.css';

function Chatbot() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [isChatOpen, setIsChatOpen] = useState(false); // State for toggle

   // Create a ref for the chatbot messages container
   const messagesContainerRef = useRef(null);

  const toggleChat = () => {
    setIsChatOpen(!isChatOpen);
  };

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = { text: input.trim(), sender: 'user' };
    setMessages((prevMessages) => [...prevMessages, userMessage]);
    setInput('');
    setLoading(true);

    try {//http://127.0.0.1:5000/chat
      const response = await axios.post('https://chat-bot-sa.onrender.com/chat', {
        message: input.trim(),
      });

      const botResponse = response.data?.response || "Sorry, I couldn't process that.";
      const botMessage = { text: botResponse, sender: 'bot' };
      setMessages((prevMessages) => [...prevMessages, botMessage]);
    } catch (error) {
      console.error('Error:', error);
      const errorMessage = {
        text: 'Sorry, something went wrong! Please try again later.',
        sender: 'bot',
      };
      setMessages((prevMessages) => [...prevMessages, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSend();
    }
  };

  // Send the first message when the chat opens
  useEffect(() => {
    if (isChatOpen) {
      const firstMessage = { text: "Hello! My name is SAI. How may I help you?", sender: 'bot' };
      setMessages([firstMessage]);
    }
  }, [isChatOpen]);

  // Scroll to the bottom whenever the messages array is updated
  useEffect(() => {
    if (messagesContainerRef.current) {
      messagesContainerRef.current.scrollTop = messagesContainerRef.current.scrollHeight;
    }
  }, [messages]); // Trigger this effect when messages change

  //icons
  const botIcon = "🤖";  // Add an emoji or an image here for the bot icon
  const userIcon = "👤";  // Add an emoji or an image here for the user icon

  return (
    <div className="chat-widget">
      {!isChatOpen && (
        <div className="chat-button" onClick={toggleChat}>
          💬
        </div>
      )}
      {isChatOpen && (
        <div className="chatbot-container">
          <div className="chatbot-header">
            <button onClick={toggleChat} className="close-button">×</button>
            Systemic Altruism Chatbot
          </div>
          <div className="chatbot-messages" ref={messagesContainerRef}>
            {messages.map((message, index) => (
              <div key={index} className={`message ${message.sender}-message`}>
              {message.sender === "user" ? (
                <span className="message-icon">{userIcon}</span>
              ) : (
                <span className="message-icon">{botIcon}</span>
              )}
              {message.text}
            </div>
            ))}
            {loading && (
              <div className="message bot-message">
                <div className="loading-dots">
                  Thinking<span>.</span><span>.</span><span>.</span>
                </div>
              </div>
            )}
          </div>
          <div className="chatbot-input">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Type your message..."
            />
            <button onClick={handleSend}>Send</button>
          </div>
        </div>
      )}
    </div>
  );
}

export default Chatbot;
