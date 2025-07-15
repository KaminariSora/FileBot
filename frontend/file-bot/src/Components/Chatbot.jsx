import { useState } from 'react';
import './Chatbot.css';

const Chatbot = () => {
    const [question, setQuestion] = useState('');
    const [answer, setAnswer] = useState('');
    const [searchQuery, setSearchQuery] = useState('');
    const [searchResults, setSearchResults] = useState([]);
    const [selectedPath, setSelectedPath] = useState('');

    // 🔍 ฟังก์ชันค้นหาไฟล์
    const handleSearchFiles = async () => {
        try {
            const res = await fetch('http://localhost:8000/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: searchQuery }),
            });

            const data = await res.json();
            setSearchResults(data);
        } catch (err) {
            console.error('Error searching files:', err);
        }
    };

    // 💬 ฟังก์ชันถามคำถามจากไฟล์
    const handleAsk = async () => {
        if (!selectedPath) {
            alert('กรุณาเลือกไฟล์ก่อน');
            return;
        }

        try {
            const res = await fetch('http://localhost:8000/ask-file', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ path: selectedPath, question }),
            });

            const data = await res.json();
            setAnswer(data.answer);
        } catch (err) {
            console.error('Error calling chatbot:', err);
            setAnswer('เกิดข้อผิดพลาด');
        }
    };

    return (
        <div className="container">
            <div className="search-box">
                <label>ค้นหาไฟล์</label>
                <input
                    type="text"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                />
                <button onClick={handleSearchFiles}>ค้นหา</button>
            </div>

            <div className="file-results">
                <h4>รายการไฟล์ที่พบ</h4>
                <ul>
                    {searchResults.map((file, index) => (
                        <li key={index}>
                            <strong>{file.name}</strong>
                            <button onClick={() => setSelectedPath(file.path)}>เลือก</button>
                        </li>
                    ))}
                </ul>
                {selectedPath && (
                    <p>
                        ✅ ไฟล์ที่เลือก: <code>{selectedPath}</code>
                    </p>
                )}
            </div>

            <div className="quesstion-box">
                <label>ถามคำถามจากไฟล์</label>
                <input
                    type="text"
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                />
                <button onClick={handleAsk}>ถาม</button>
            </div>

            <div className="answer-box">
                <h6>{answer}</h6>
            </div>
        </div>
    );
};

export default Chatbot;
