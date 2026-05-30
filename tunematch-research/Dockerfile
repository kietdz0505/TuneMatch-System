# Sử dụng Python 3.10
FROM python:3.10-slim

# Thiết lập thư mục làm việc
WORKDIR /app

# Cài đặt các thư viện hệ thống cần thiết (nếu có dùng librosa/numpy)
RUN apt-get update && apt-get install -y \
    build-essential \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Copy file requirements.txt (bạn nên tạo file này chứa các thư viện như fastapi, uvicorn, librosa)
COPY requirements.txt .

# Cài đặt dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ source code vào container
COPY . .

# Expose port cho FastAPI
EXPOSE 8000

# Lệnh chạy API (thay 'main:app' bằng tên file và đối tượng app của bạn)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]