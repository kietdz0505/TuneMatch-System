import cloudscraper  
from bs4 import BeautifulSoup
from music21 import pitch
import re
import time
import random

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
}

def note_to_hz(note_name):
    try:
        note_name = note_name.strip()
        note_name = note_name.replace("♯", "#").replace("♭", "-")
        p = pitch.Pitch(note_name)
        return round(p.frequency, 2)
    except Exception:
        return None

def crawl_artist_profile(artist_name, url, scraper):
    print(f"Đang cào dữ liệu trực tiếp của: {artist_name}...")
    try:
        response = scraper.get(url, headers=HEADERS, timeout=15)
        
        if response.status_code != 200:
            print(f"Không thể truy cập {artist_name}. Mã lỗi HTTP: {response.status_code}")
            return []
            
        soup = BeautifulSoup(response.content, "html.parser")
        main_post = soup.find("div", class_="message")
        
        if not main_post:
            print(f"Không tìm thấy khối nội dung bài viết của {artist_name}.")
            return []

        song_pitches = {}
        note_regex = re.compile(r'^\s*([A-G][♯♭#]?\d)')
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

        artist_songs = []
        for song_name, pitches in song_pitches.items():
            if pitches:
                pitches.sort(key=lambda x: x.ps)
                min_pitch = pitches[0]
                max_pitch = pitches[-1]
                
                min_note_str = min_pitch.nameWithOctave.replace("-", "b")
                max_note_str = max_pitch.nameWithOctave.replace("-", "b")
                
                artist_songs.append({
                    "title": song_name,
                    "artist": artist_name,
                    "min_note": min_note_str,
                    "min_frequency": round(min_pitch.frequency, 2),
                    "max_note": max_note_str,
                    "max_frequency": round(max_pitch.frequency, 2)
                })
                
        print(f"Thành công! Trích xuất được {len(artist_songs)} bài hát của {artist_name}.")
        return artist_songs

    except Exception as e:
        print(f"Lỗi khi xử lý {artist_name}: {str(e)}")
        return []

def main():
    artists_to_crawl = [
        {"name": "Bruno Mars", "url": "https://therangeplanet.proboards.com/thread/230/bruno-mars"},
        {"name": "Charlie Puth", "url": "https://therangeplanet.proboards.com/thread/450/charlie-puth"},
        {"name": "Ariana Grande", "url": "https://therangeplanet.proboards.com/thread/18/ariana-grande"},
        {"name": "Adele", "url": "https://therangeplanet.proboards.com/thread/58/adele"},
        {"name": "Billie Eilish", "url": "https://therangeplanet.proboards.com/thread/424/billie-eilish"},
        {"name": "Justin Bieber", "url": "https://therangeplanet.proboards.com/thread/357/justin-bieber"},
        {"name": "Ed Sheeran", "url": "https://therangeplanet.proboards.com/thread/100/ed-sheeran"},
        {"name": "Sam Smith", "url": "https://therangeplanet.proboards.com/thread/254/sam-smith"},
        {"name": "Lady Gaga", "url": "https://therangeplanet.proboards.com/thread/92/lady-gaga"},
        {"name": "Zayn Malik", "url": "https://therangeplanet.proboards.com/thread/643/zayn"},
        {"name": "Sia", "url": "https://therangeplanet.proboards.com/thread/201/sia"},
        {"name": "The Weeknd", "url": "https://therangeplanet.proboards.com/thread/234/weeknd"}
    ]

    all_songs_data = []
    
    scraper = cloudscraper.create_scraper()

    print(f"Bắt đầu chiến dịch cào dữ liệu lớn TuneMatch ({len(artists_to_crawl)} ca sĩ)...")
    
    for item in artists_to_crawl:
        songs = crawl_artist_profile(item["name"], item["url"], scraper)
        all_songs_data.extend(songs)
        
        if item != artists_to_crawl[-1]:
            sleep_time = random.uniform(3.0, 5.0)
            print(f"Nghỉ {round(sleep_time, 2)} giây trước khi sang ca sĩ tiếp theo...")
            time.sleep(sleep_time)

    print(f"\nTỔNG KẾT: Đã thu thập thành công {len(all_songs_data)} bài hát sạch của tất cả ca sĩ!")
    
    if len(all_songs_data) == 0:
        print("Không thu thập được dữ liệu nào. Vui lòng kiểm tra lại cấu hình.")
        return

    output_sql = "multi_artists_songs.sql"
    with open(output_sql, "w", encoding="utf-8") as f:
        f.write("INSERT INTO songs (title, artist, min_note, min_frequency, max_note, max_frequency) VALUES \n")
        for i, song in enumerate(all_songs_data):
            comma = "," if i < len(all_songs_data) - 1 else ";"
            safe_title = song['title'].replace("'", "''")
            line = f"('{safe_title}', '{song['artist']}', '{song['min_note']}', {song['min_frequency']}, '{song['max_note']}', {song['max_frequency']}){comma}\n"
            f.write(line)

    print(f"ĐÃ XUẤT THÀNH CÔNG FILE SQL LỚN: {output_sql}!")

if __name__ == "__main__":
    main()