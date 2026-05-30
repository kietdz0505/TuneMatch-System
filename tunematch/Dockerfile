# Sử dụng image chính thức và ổn định hơn
FROM eclipse-temurin:21-jre-jammy
# Thiết lập thư mục làm việc trong container
WORKDIR /app

# Copy file jar đã build
COPY target/*.jar app.jar

# Expose port
EXPOSE 8080

# Chạy ứng dụng
ENTRYPOINT ["java", "-jar", "app.jar"]