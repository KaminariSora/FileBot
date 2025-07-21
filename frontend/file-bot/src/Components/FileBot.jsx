import { useState } from 'react';
import './FileBot.css';

const FileBot = () => {
    const [question, setQuestion] = useState('');
    const [answer, setAnswer] = useState('');
    const [pathValue, setPathValue] = useState('');
    const [searchQuery, setSearchQuery] = useState('');
    const [searchResults, setSearchResults] = useState([]);
    const [selectedPath, setSelectedPath] = useState('');
    const [isPathLoading, setIsPathLoading] = useState(false)
    const [isLoading, setIsLoading] = useState(false);
    const [status, setStatus] = useState(false)

    const handleSearchPathValue = async () => {
        setIsPathLoading(true);
        try {
            const res = await fetch('http://localhost:8000/search-path', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ path: pathValue }),
            });
            const data = await res.json();
            console.log("search-path response:", data);

            if (data.exists) {
                setStatus(true);
                setAnswer(`พบ path: ${data.path}`);
            } else {
                setStatus(false);
                setAnswer(`ไม่พบ path: ${data.path}`);
            }
        } catch (err) {
            console.error('Error searching path:', err);
            setStatus(false);
            setAnswer('เกิดข้อผิดพลาดในการตรวจสอบ path');
        } finally {
            setIsPathLoading(false);
        }
    };


    const handleSearchFiles = async () => {
        setIsLoading(true);
        try {
            const res = await fetch('http://localhost:8000/intent-text', {
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
            setAnswer('เกิดข้อผิดพลาดในการค้นหาไฟล์');
        } finally {
            setIsLoading(false);
        }
    };

    const handleOpenFile = async (filepath) => {
        setIsLoading(true);
        try {
            const res = await fetch('http://localhost:8000/open-file', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ filepath }),
            });

            const data = await res.json();
            setAnswer(data.message || 'เปิดไฟล์เรียบร้อยแล้ว');
        } catch (err) {
            console.error('Error opening file:', err);
            setAnswer('เกิดข้อผิดพลาดในการเปิดไฟล์');
        } finally {
            setIsLoading(false);
        }
    };

    const handleAsk = async () => {
        if (!selectedPath) {
            setAnswer('กรุณาเลือกไฟล์ก่อน');
            return;
        }

        setIsLoading(true);
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
            console.error('Error calling FileBot:', err);
            setAnswer('เกิดข้อผิดพลาดในการถามคำถาม');
        } finally {
            setIsLoading(false);
        }
    };

    const handleSelectFile = (file) => {
        setSelectedPath(file.path);
        setAnswer(`เลือกไฟล์: ${file.name}`);
    };

    const handlePathClear = () => {
        setPathValue('');
        setSearchResults([]);
        setStatus(false);
    };

    const handleSearchClear = () => {
        setSearchQuery('');
        setSearchResults([]);
        setSelectedPath('');
        setQuestion('');
        setAnswer('');
    };

    return (
        <div className='file-bot-body'>
            <div className="file-bot-container">
                <div className="path-box">
                    <label>ใส่ Path ที่ต้องการให้ค้นหา</label>
                    <input
                        type="text"
                        value={pathValue}
                        onChange={(e) => setPathValue(e.target.value)}
                        placeholder="ใส่ Path บน PC เช่น D:\Path\Path"
                    />
                    <div className="button-group">
                        <button
                            onClick={handleSearchPathValue}
                            disabled={isPathLoading || !pathValue.trim()}
                            className={isPathLoading ? 'PathLoading' : ''}
                        >
                            {isPathLoading ? 'กำลังค้นหาPath...' : 'ค้นหา Path'}
                        </button>
                        <button onClick={handlePathClear} className="clear-btn">
                            ล้างข้อมูล Path
                        </button>
                    </div>
                    {status === true && <div>ยืนยันว่า Path มีอยู่จริง</div>}
                    {status === false && <div>กรุณาใส่ Path ที่ต้องการให้ค้นหา</div>}
                </div>
                {/* Search Section */}
                <div className="search-box">
                    <label>ค้นหาไฟล์</label>
                    <input
                        type="text"
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                        placeholder="พิมพ์ชื่อไฟล์ หรือ นามสกุล เช่น report.pdf, .xlsx"
                        onKeyPress={(e) => e.key === 'Enter' && handleSearchFiles()}
                    />
                    <div className="button-group">
                        <button
                            onClick={handleSearchFiles}
                            disabled={isLoading || !searchQuery.trim()}
                            className={isLoading ? 'loading' : ''}
                        >
                            {isLoading ? 'กำลังค้นหา...' : 'ค้นหา'}
                        </button>
                        <button onClick={handleSearchClear} className="clear-btn">
                            ล้างข้อมูล
                        </button>
                    </div>
                </div>

                {/* File Results Section */}
                <div className="file-results">
                    <h4>รายการไฟล์ที่พบ ({searchResults.length} ไฟล์)</h4>
                    <ul>
                        {searchResults.map((file, index) => (
                            <li key={index} className={selectedPath === file.path ? 'selected' : ''}>
                                <div className="file-info">
                                    <strong>{file.name}</strong>
                                    <small>{file.path}</small>
                                </div>
                                <div className="file-actions">
                                    <button
                                        onClick={() => handleSelectFile(file)}
                                        className="select-btn"
                                    >
                                        เลือก
                                    </button>
                                    <button
                                        onClick={() => handleOpenFile(file.path)}
                                        className="open-btn"
                                        disabled={isLoading}
                                    >
                                        เปิดไฟล์
                                    </button>
                                </div>
                            </li>
                        ))}
                    </ul>
                    {searchResults.length === 0 && searchQuery && (
                        <p className="no-results">ไม่พบไฟล์ที่ตรงกับการค้นหา</p>
                    )}
                    {selectedPath && (
                        <div className="selected-file">
                            <p>
                                ไฟล์ที่เลือก: <code>{selectedPath}</code>
                            </p>
                        </div>
                    )}
                </div>

                {/* Question Section */}
                <div className="question-box">
                    <label>ถามคำถามจากไฟล์</label>
                    <input
                        type="text"
                        value={question}
                        onChange={(e) => setQuestion(e.target.value)}
                        placeholder="พิมพ์คำถามที่ต้องการถามจากไฟล์"
                        onKeyPress={(e) => e.key === 'Enter' && handleAsk()}
                    />
                    <button
                        onClick={handleAsk}
                        disabled={isLoading || !selectedPath || !question.trim()}
                        className={isLoading ? 'loading' : ''}
                    >
                        {isLoading ? 'กำลังประมวลผล...' : 'ถาม'}
                    </button>
                </div>

                {/* Answer Section */}
                <div className="answer-box">
                    <h6>{answer || 'คำตอบจะปรากฏที่นี่...'}</h6>
                </div>
            </div>
        </div>
    );
}

export default FileBot;