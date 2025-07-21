import './App.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import FileBot from './Components/FileBot';
import ChatBot from './Components/ChatBot';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<ChatBot />} />
        <Route path="/ChatBot" element={<ChatBot />} />
        <Route path="/FileBot" element={<FileBot />} />
      </Routes>
    </Router>
  );
}

export default App;
