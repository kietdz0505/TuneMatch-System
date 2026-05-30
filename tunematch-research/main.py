from fastapi import FastAPI, UploadFile, File
import librosa
import numpy as np
import os
import shutil

app = FastAPI(title="TuneMatch Audio API")

@app.post("/analyze")
async def analyze_audio(file: UploadFile = File(...)):
    temp_file_path = f"temp_{file.filename}"
    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        y, sr = librosa.load(temp_file_path, sr=None)
        
        f0, voiced_flag, voiced_probs = librosa.pyin(
            y, 
            fmin=librosa.note_to_hz('C2'), 
            fmax=librosa.note_to_hz('C6')
        )
        
        frequencies = f0[~np.isnan(f0)]
        
        if len(frequencies) == 0:
            return {"status": "error", "message": "Không tìm thấy cao độ rõ ràng"}

        min_hz = float(np.min(frequencies))
        max_hz = float(np.max(frequencies))
        
        min_note = librosa.hz_to_note(min_hz)
        max_note = librosa.hz_to_note(max_hz)
        
        return {
            "status": "success",
            "data": {
                "min_frequency_hz": round(min_hz, 2),
                "max_frequency_hz": round(max_hz, 2),
                "min_note": min_note,
                "max_note": max_note
            }
        }
        
    except Exception as e:
        return {"status": "error", "message": str(e)}
        
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)