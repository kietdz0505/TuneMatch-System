# TuneMatch System

Hệ thống phân tích giọng hát (Vocal Analysis) và gợi ý bài hát dựa trên khoảng âm (Vocal Range). Hệ thống bao gồm một Backend Java Spring Boot, một Microservice Python để xử lý âm thanh và giao diện Frontend để tương tác.

## 🚀 Tính năng nổi bật
- **Phân tích giọng hát:** Upload file âm thanh để hệ thống tự động xác định dải tần (Hz) và nốt nhạc (Note).
- **Gợi ý thông minh:** Tự động truy vấn Database để tìm các bài hát có khoảng âm phù hợp với người dùng.
- **Microservices:** Kiến trúc tách biệt giúp dễ dàng bảo trì và mở rộng.
- **Dockerized:** Cài đặt và chạy toàn bộ hệ thống bằng một dòng lệnh.

## 🛠 Công nghệ sử dụng
- **Backend:** Java, Spring Boot, Spring Data JPA, MySQL.
- **AI/Audio Analysis:** Python (librosa/scipy), FastAPI/Flask.
- **Frontend:** React, Vite, Tailwind CSS.
- **Infrastructure:** Docker & Docker Compose.

## 📂 Cấu trúc dự án
```text
TuneMatch-System/
├── tunematch/          # Java Spring Boot Backend
├── tunematch-research/ # Python Analysis API
├── tunematch-frontend/ # React Frontend
├── docker-compose.yml  # File điều phối Docker
└── README.md
```
## ⚙️ Hướng dẫn cài đặt & Triển khai toàn tập

Để triển khai dự án này dưới máy local, bạn không cần phải cài đặt thủ công Java, Python hay MySQL. Tất cả đã được cấu hình tự động trong môi trường ảo hóa Docker.

### Yêu cầu tiên quyết
* Đã cài đặt **Git**.
* Đã cài đặt **Docker Desktop** (Đảm bảo ứng dụng Docker đã được bật lên trước khi thực hiện các lệnh bên dưới).

### Các bước thực hiện chi tiết

#### Bước 1: Sao chép mã nguồn về máy local
Mở Git Bash hoặc Terminal tại thư mục bạn muốn chứa dự án trên máy tính và chạy tổ hợp lệnh:
```bash
git clone https://github.com/kietdz0505/TuneMatch-System.git
cd TuneMatch-System
```

### Bước 2: Khởi chạy môi trường với Docker Compose

Tại thư mục gốc của dự án TuneMatch-System (nơi có chứa file docker-compose.yml), hãy chạy lệnh sau để hệ thống tự động tải các base image, đóng gói toàn bộ mã nguồn và kích hoạt các container chạy ngầm:
```bash
docker-compose up -d --build
```
### Bước 3: Kiểm tra trạng thái vận hành của các dịch vụ

Đảm bảo tất cả các container đã hoạt động bình thường bằng cách kiểm tra danh sách tiến trình:
```bash
docker ps
```
Nếu màn hình Terminal hiển thị đầy đủ thông tin các container tương ứng với Frontend, Backend, API Research và cơ sở dữ liệu MySQL đều đang ở trạng thái Up, hệ thống đã sẵn sàng hoạt động.
Cổng truy cập mặc định của các thành phần dịch vụ

    Giao diện Frontend (React): http://localhost:5173
