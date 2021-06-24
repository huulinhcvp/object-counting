# Hướng dẫn cài đặt

1. Tạo conda virtual environment với

```
conda create --name <env> --file requirements.txt
```

2. Khởi chạy ứng dụng

Trên terminal, đảm bảo đến đúng đường dẫn tới project, chạy lệnh sau:

```
python app.py
```

# Chi tiết về các folders, filenames

1. File app.py
```
File này là entry point, khởi chạy ứng dụng
```

2. Thư mục frames
```
Thư mục này chứa giao diện của ứng dụng
```

3. Thư mục resources
```
Thư mục này chứa các tài nguyên của ứng dụng, ảnh mặc định và lưu trữ ảnh đầu ra
```

4. File processing.py
```
File này chứa các chuỗi xử lý cho các ảnh đầu vào, là lõi của ứng dụng
```

5. File counter.py
```
File này chứa 2 hàm đếm đối tượng. Đếm dựa trên các thành phần liên thông hoặc đếm dựa trên contours
```

6. File test.py
```
File dùng để thử nghiệm khi tiến hành thực nghiệm với các tham số đầu vào khác nhau cho chuỗi xử lý ảnh
```

7. File docs.md
```
File này chứa tài liệu hướng dẫn các bước xử lý ảnh
```

8. File requirements.txt
```
File này chứa các yêu cầu về cấu hình
```
