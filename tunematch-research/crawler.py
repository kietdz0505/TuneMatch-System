from bs4 import BeautifulSoup
from music21 import pitch
import re
import os

def note_to_hz(note_name):
    try:
        note_name = note_name.strip()
        note_name = note_name.replace("♯", "#").replace("♭", "-")
        p = pitch.Pitch(note_name)
        return round(p.frequency, 2)
    except Exception:
        return None

def analyze_local_html():
    file_path = "page.html"
    
    if not os.path.exists(file_path):
        print(f"Không tìm thấy file {file_path}! Vui lòng kiểm tra lại thư mục dự án.")
        return

    print(f"Đang đọc và phân tích dữ liệu nhạc lý từ file local: {file_path}...")
    
    with open(file_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, "html.parser")
    main_post = soup.find("div", class_="message")
    
    if not main_post:
        print("Không tìm thấy khối bài viết nào chứa class 'message' trong file HTML.")
        return

    song_pitches = {}
    note_regex = re.compile(r'^\s*([A-G][♯♭#]?\d)')
    current_note = None
    current_pitch_obj = None

    for text_string in main_post.strings:
        cleaned_str = text_string.strip()
        if not cleaned_str:
            continue
            
        match = note_regex.match(cleaned_str)
        if match:
            current_note = match.group(1)
            normalized_note = current_note.replace("♯", "#").replace("♭", "-")
            try:
                current_pitch_obj = pitch.Pitch(normalized_note)
            except Exception:
                current_pitch_obj = None
                
        if current_pitch_obj:
            songs_found = re.findall(r'"([^"]+)"', cleaned_str)
            for song in songs_found:
                song_name = song.strip()
                if (len(song_name) > 60 
                        or "singing" in song_name.lower() 
                        or song_name in [",", ", ,", "", ".", "uncredited"]
                        or len(song_name) <= 1):
                    continue
                    
                if song_name not in song_pitches:
                    song_pitches[song_name] = []
                song_pitches[song_name].append(current_pitch_obj)

    songs_data = []
    for song_name, pitches in song_pitches.items():
        if pitches:
            pitches.sort(key=lambda x: x.ps)
            
            min_pitch = pitches[0]
            max_pitch = pitches[-1]
            
            min_note_str = min_pitch.nameWithOctave.replace("-", "b")
            max_note_str = max_pitch.nameWithOctave.replace("-", "b")
            
            songs_data.append({
                "title": song_name,
                "artist": "The Weeknd",
                "min_note": min_note_str,
                "min_frequency": round(min_pitch.frequency, 2),
                "max_note": max_note_str,
                "max_frequency": round(max_pitch.frequency, 2)
            })

    print(f"Trích xuất thành công {len(songs_data)} bài hát SẠCH từ profile của The Weeknd!")
    
    if len(songs_data) == 0:
        print("Vẫn không tìm thấy dữ liệu. Có thể cấu trúc trang HTML này thuộc phiên bản giao diện khác.")
        return
        
    output_sql = "data_songs.sql"
    with open(output_sql, "w", encoding="utf-8") as f:
        f.write("INSERT INTO songs (title, artist, min_note, min_frequency, max_note, max_frequency) VALUES \n")
        for i, song in enumerate(songs_data):
            comma = "," if i < len(songs_data) - 1 else ";"
            safe_title = song['title'].replace("'", "''")
            line = f"('{safe_title}', '{song['artist']}', '{song['min_note']}', {song['min_frequency']}, '{song['max_note']}', {song['max_frequency']}){comma}\n"
            f.write(line)
            
    print(f"Đã ghi dữ liệu ra file: {output_sql} thành công!")

if __name__ == "__main__":
    analyze_local_html()