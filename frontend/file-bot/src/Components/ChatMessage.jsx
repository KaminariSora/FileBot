const ChatMessage = ({chat}) => {
    return (
        <div className={`message ${chat.role === "assistant" ? 'bot' : 'user'}-message`}>
            {chat.role === "assistant"}
            <p className='message-text'>{chat.text}</p>
        </div>
    )
}

export default ChatMessage