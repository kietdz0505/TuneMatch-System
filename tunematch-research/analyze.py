import librosa
import numpy as np
import warnings
import os

warnings.filterwarnings("ignore")

def analyze_vocal_range(file_path):
    if not os.path.exists(file_path):
        print(f"Lỗi: Không tìm thấy file '{file_path}' trong thư mục hiện tại!")
        print("Vui lòng kiểm tra lại tên file và đuôi file (ví dụ: .mp3, .wav).")
        return

    print(f"🎵 Đang đọc và phân tích file: {file_path}...")
    print("Quá trình này có thể mất vài giây tùy thuộc vào độ dài của file...")
    
    try:
       
        y, sr = librosa.load(file_path, sr=None)
        f0, voiced_flag, voiced_probs = librosa.pyin(
            y, 
            fmin=librosa.note_to_hz('C2'), 
            fmax=librosa.note_to_hz('C6')  
        )
        
        frequencies = f0[~np.isnan(f0)]
        
        if len(frequencies) == 0:
            print("Cảnh báo: Không tìm thấy cao độ rõ ràng nào trong file âm thanh này.")
            return

        min_hz = np.min(frequencies)
        max_hz = np.max(frequencies)
        
        min_note = librosa.hz_to_note(min_hz)
        max_note = librosa.hz_to_note(max_hz)
        
        print("\n" + "="*30)
        print("KẾT QUẢ PHÂN TÍCH CAO ĐỘ:")
        print("="*30)
        print(f"Tần số thấp nhất: {min_hz:.2f} Hz -> Nốt nhạc: {min_note}")
        print(f"Tần số cao nhất: {max_hz:.2f} Hz -> Nốt nhạc: {max_note}")
        print("="*30)
        print("Chạy test thành công! Hệ thống đã nhận diện được âm thanh.")

    except Exception as e:
        print(f"Đã xảy ra lỗi trong quá trình xử lý file: {str(e)}")

FILE_NAME_TO_TEST = 'test.mp3' 

analyze_vocal_range(FILE_NAME_TO_TEST)