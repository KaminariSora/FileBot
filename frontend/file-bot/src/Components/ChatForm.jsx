import { useRef } from 'react'
import { useNavigate } from 'react-router-dom';
import PaperPlane from './icons/paperPlane'

const ChatForm = ({chatHistory, setChatHistory, getModelResponse}) => {
    const inputRef = useRef();
    const navigate = useNavigate()

    const handleFormSubmit = (e) => {
        e.preventDefault()
        const userMessage = inputRef.current.value.trim()
        
        if(userMessage === "enter searching file mode") {
            navigate('/FileBot')
        } else {
            if(!userMessage) return;
            inputRef.current.value = "";
    
            setChatHistory(history => [...history, {role: "user", text: userMessage}]);
    
            setTimeout(() => {
                setChatHistory(history => [...history, {role: "model", text: "Thinking..."}])
                
                getModelResponse([...chatHistory, {role: "user", text: userMessage}])
            }, 600);
        }

    }

    return (
        <form action="#" className="chat-form" onSubmit={handleFormSubmit}>
            <input ref={inputRef} type='text' className='message-input' placeholder='type message...' required></input>
            <button className=''><PaperPlane /></button>
        </form>
    )
}

export default ChatForm