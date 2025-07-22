import { useNavigate } from 'react-router-dom'
import { useState, useEffect } from 'react'
import './ConfirmPopUp.css'

const ConfirmPopUp = ({setPopUpOpen}) => {
    const navigate = useNavigate()
    const [showClass, setShowClass] = useState(false)

    useEffect(() => {
    const timeout = setTimeout(() => setShowClass(true), 10)
    return () => clearTimeout(timeout)
  }, [])

    const handleOkButton = () => {
        navigate('/FileBot')
        console.log("OK")
    }

    const handleCanclePopup = () => {
        setPopUpOpen(false)
        console.log("set")
    }

    return (
        <div className={`confirm-popup ${showClass ? 'show' : ''}`}>
            <p className='heading-popup'>คุณต้องการเปิด File searching mode หรือไม่?</p>
            <div className='choice-selection' onClick={handleOkButton}>ตกลง</div>
            <div className='choice-selection' onClick={handleCanclePopup}>ยกเลิก</div>
        </div>
    )
}

export default ConfirmPopUp