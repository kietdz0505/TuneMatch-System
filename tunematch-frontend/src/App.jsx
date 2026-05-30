import React, { useState, useRef } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const [audioUrl, setAudioUrl] = useState(null);
  
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);

  const [result, setResult] = useState(() => {
    const savedResult = localStorage.getItem('tunematch_result');
    return savedResult ? JSON.parse(savedResult) : null;
  });

  const [savedFileName, setSavedFileName] = useState(() => {
    return localStorage.getItem('tunematch_filename') || '';
  });

  // Xử lý khi chọn file từ máy tính
  const handleFileChange = (e) => {
    if (loading || isRecording) return; // Chặn đổi file khi hệ thống đang bận

    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      setSavedFileName(selectedFile.name);
      localStorage.setItem('tunematch_filename', selectedFile.name);
      setAudioUrl(null); 
    }
  };

  const startRecording = async () => {
    if (loading || isRecording) return; 

    audioChunksRef.current = [];
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorderRef.current = new MediaRecorder(stream);
      
      mediaRecorderRef.current.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      mediaRecorderRef.current.onstop = () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/wav' });
        const recordedFile = new File([audioBlob], "recorded_vocal.wav", { type: 'audio/wav' });
        
        setFile(recordedFile);
        setSavedFileName("recorded_vocal.wav");
        localStorage.setItem('tunematch_filename', "recorded_vocal.wav");
        setAudioUrl(URL.createObjectURL(audioBlob));
      };

      mediaRecorderRef.current.start();
      setIsRecording(true);
    } catch (err) {
      console.error("Microphone Access Error:", err);
      alert("Hệ thống không thể kết nối tới Microphone! Vui lòng cấp quyền ở trình duyệt.");
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      mediaRecorderRef.current.stream.getTracks().forEach(track => track.stop());
      setIsRecording(false);
    }
  };

  const handleUpload = async () => {
    if (!file || loading || isRecording) return; 

    const formData = new FormData();
    formData.append('file', file);
    setLoading(true);

    try {
      const response = await axios.post('http://localhost:8080/api/vocal/analyze-and-recommend', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      
      setResult(response.data);
      localStorage.setItem('tunematch_result', JSON.stringify(response.data));
    } catch (error) {
      console.error("API Connection Error:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    if (loading || isRecording) return;
    
    setFile(null);
    setResult(null);
    setSavedFileName('');
    setAudioUrl(null);
    localStorage.removeItem('tunematch_result');
    localStorage.removeItem('tunematch_filename');
  };

  return (
    <div className="container">
      <div className="title-section">
        <h1>🎵 TuneMatch Research</h1>
        <p>Hệ thống AI phân tích khoảng giọng và đề xuất bài hát thời gian thực</p>
      </div>

      <div className="card">
        <h3 className="card-title">Bước 1: Cung cấp dữ liệu đầu vào mẫu</h3>
        
        <div className="method-group">
          <div className="file-input-wrapper" style={{ opacity: isRecording ? 0.5 : 1 }}>
            <label style={{ fontWeight: '600', display: 'block', marginBottom: '8px' }}>📁 Tải file nhạc lên</label>
            <input 
              type="file" 
              accept="audio/*" 
              onChange={handleFileChange} 
              disabled={isRecording || loading} 
            />
          </div>

          <div className="divider">HOẶC</div>

          <div className="record-box">
            {!isRecording ? (
              <button onClick={startRecording} className="btn btn-danger" disabled={loading || !!(file && !audioUrl)}>
                🔴 Ghi âm trực tiếp
              </button>
            ) : (
              <button onClick={stopRecording} className="btn btn-success pulse">
                ⏹️ Dừng ghi âm
              </button>
            )}
          </div>
        </div>

        {audioUrl && (
          <div className="audio-preview">
            <p style={{ margin: '0 0 8px 0', fontSize: '0.9rem', color: 'var(--primary)', fontWeight: '600' }}>🎧 Nghe lại bản ghi âm của bạn:</p>
            <audio src={audioUrl} controls style={{ width: '100%' }} />
          </div>
        )}

        {savedFileName && (
          <p style={{ margin: '20px 0 0 0', fontSize: '0.9rem', color: 'var(--text-muted)' }}>
            🎯 Đối tượng sẵn sàng: <strong>{savedFileName}</strong>
          </p>
        )}

        <div className="action-bar">
          <button onClick={handleUpload} className="btn btn-primary" disabled={loading || isRecording || !file}>
            {loading ? "⌛ Đang phân tích tín hiệu..." : "🚀 Phân tích & Gợi ý ngay"}
          </button>

          {result && (
            <button onClick={handleClear} className="btn btn-secondary" disabled={loading || isRecording}>
              🗑️ Xóa kết quả cũ
            </button>
          )}
        </div>
      </div>

      {result && result.status === "success" && (
        <div>
          <div className="card">
            <h3 className="card-title" style={{ color: 'var(--success)', marginBottom: '15px' }}>🎤 Khoảng Giọng Của Bạn</h3>
            <div className="range-display">
              <div className="range-item">
                <p>Nốt thấp nhất</p>
                <h2 className="note-low">{result.user_vocal_range.min_note}</h2>
                <small>{result.user_vocal_range.min_hz} Hz</small>
              </div>
              <div className="range-item" style={{ borderLeft: '1px solid var(--border)' }}>
                <p>Nốt cao nhất</p>
                <h2 className="note-high">{result.user_vocal_range.max_note}</h2>
                <small>{result.user_vocal_range.max_hz} Hz</small>
              </div>
            </div>
          </div>

          <h3 className="card-title">🎶 Bài hát phù hợp với bạn</h3>
          {result.recommended_songs.length > 0 ? (
            <div className="table-container">
              <table className="custom-table">
                <thead>
                  <tr>
                    <th>Tên Bài Hát</th>
                    <th>Ca Sĩ Execution</th>
                    <th>Khoảng Tone Phù Hợp</th>
                  </tr>
                </thead>
                <tbody>
                  {result.recommended_songs.map((song, index) => (
                    <tr key={song.id || index}>
                      <td><strong>{song.title}</strong></td>
                      <td>{song.artist}</td>
                      <td>
                        <span className="badge">
                          {song.minNote} → {song.maxNote}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <div className="card" style={{ textAlign: 'center', color: 'var(--text-muted)' }}>
              😔 Không tìm thấy bài hát mẫu nào tương thích hoàn hảo với khoảng giọng hiện tại của bạn.
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default App;