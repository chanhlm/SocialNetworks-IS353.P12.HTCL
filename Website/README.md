# Website gợi ý phim

Dự án này liên quan đến một website gợi ý phim sử dụng thuật toán khám phá cộng đồng lan truyền trong mạng xã hội. Hãy làm theo các bước dưới đây để thiết lập và chạy ứng dụng web.

## Hướng dẫn thiết lập

1. **Khởi động API**  
   Mở terminal và chạy lệnh sau để khởi động API
   ```bash
      uvicorn main:app --host 127.0.0.1 --port 8000 --reload
   ```
#### Chú ý:
   - Dùng `--reload` khi phát triển: Giúp tự động cập nhật code khi có thay đổi, thuận tiện cho việc thử nghiệm và phát triển.
   - Không dùng `--reload` khi sản xuất: Để đảm bảo hiệu suất và bảo mật, chạy server với cấu hình ổn định mà không tự động tải lại code.
   
2 **Chạy ứng dụng web**  
   Chạy file py bằng lệnh
   ```bash
   streamlit run index.py
   ```
