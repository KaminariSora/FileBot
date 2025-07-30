import { useState } from 'react'
import './ChatBot.css'
import ChatForm from './ChatForm'
import ChatMessage from './ChatMessage'

const ChatBot = () => {
    const [chatHistory, setChatHistory] = useState([]);

    const getModelResponse = async (history) => {
        const updateHistory = (text) => {
            setChatHistory(prev => [
                ...prev.filter(msg => msg.text !== "Thinking..."),
                { role: "assistant", text }
            ]);
        }

        history = history.map(({ role, text }) => ({ role, parts: [{ text }] }));
        const requestOptions = {
            method: 'POST',
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ contents: history })
        }
        try {
            const response = await fetch("http://localhost:8000/mcp-run", requestOptions)
            const data = await response.json()
            if (!response.ok) throw new Error(data.error.message || "Something went wrong!")

            const apiResponseText = data.candidate[0].contents.part[0].text.replace(/\*\*(.*?)\*\*/g, "$1").trim()
            updateHistory(apiResponseText)
        } catch (error) {
            console.log(error)
        }
    }
    return (
        <div className='chatbot-body'>
            <div className="container">
                <div className="chat-header">
                    <div className="header-info">
                        <h2 className="logo-text">Main Bot</h2>
                    </div>
                </div>
                <div className='chat-body'>
                    <div className='message bot-message'>
                        <p className='message-text'>Hello, May I help you? (สวัสดี มีอะไรให้ช่วยไหม)</p>
                    </div>
                    {chatHistory.map((chat, index) => (
                        <ChatMessage key={index} chat={chat} />
                    ))}
                </div>
                <ChatForm chatHistory={chatHistory} setChatHistory={setChatHistory} getModelResponse={getModelResponse} />
            </div>
        </div>
    )
}

export default ChatBot