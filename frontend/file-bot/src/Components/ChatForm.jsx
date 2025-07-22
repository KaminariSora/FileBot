import { useRef, useState } from 'react'
import { useNavigate } from 'react-router-dom';
import PaperPlane from './icons/paperPlane'
import PlusCircle from './icons/plus';
import ConfirmPopUp from './ConfirmPopUp';

const ChatForm = ({ chatHistory, setChatHistory, getModelResponse }) => {
    const inputRef = useRef();
    const navigate = useNavigate()
    const [popUpOpen, setPopUpOpen] = useState(false)

    const handleFormSubmit = (e) => {
        e.preventDefault()
        const userMessage = inputRef.current.value.trim()

        if (userMessage === "enter searching file mode") {
            navigate('/FileBot')
        } else {
            if (!userMessage) return;
            inputRef.current.value = "";

            setChatHistory(history => [...history, { role: "user", text: userMessage }]);

            setTimeout(() => {
                setChatHistory(history => [...history, { role: "assistant", text: "Thinking..." }])

                getModelResponse([...chatHistory, { role: "user", text: userMessage }])
            }, 600);
        }

    }

    const handlePlusButtonClick = () => {
        setPopUpOpen(true)
    }

    return (
        <div className='chat-footer'>
            {popUpOpen && <ConfirmPopUp setPopUpOpen={setPopUpOpen}/>}
            <button className='plus-button' onClick={handlePlusButtonClick}><PlusCircle /></button>
            <form action="#" className="chat-form" onSubmit={handleFormSubmit}>
                <input ref={inputRef} type='text' className='message-input' placeholder='type message...' required></input>
                <button className=''><PaperPlane /></button>
            </form>
        </div>
    )
}

export default ChatForm