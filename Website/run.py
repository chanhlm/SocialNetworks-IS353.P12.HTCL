from subprocess import Popen, PIPE
import signal
import sys
import threading

def run_streamlit():
    return Popen(["streamlit", "run", "./Streamlit/main.py"], stdout=PIPE, stderr=PIPE, text=True)

def run_uvicorn():
    return Popen(["uvicorn", "API.main:app", "--host", "127.0.0.1", "--port", "8000", "--reload"], stdout=PIPE, stderr=PIPE, text=True)

def read_output(process, stream_name):
    """Đọc đầu ra từ tiến trình và in ra màn hình."""
    for line in iter(process.stdout.readline, ''):
        if line:
            sys.stdout.write(f"[{stream_name}] {line}")
            sys.stdout.flush()
    process.stdout.close()

def read_error(process, stream_name):
    """Đọc đầu ra lỗi từ tiến trình và in ra màn hình."""
    for line in iter(process.stderr.readline, ''):
        if line:
            sys.stderr.write(f"[{stream_name} ERROR] {line}")
            sys.stderr.flush()
    process.stderr.close()

if __name__ == "__main__":
    try:
        # Khởi động tiến trình
        streamlit_process = run_streamlit()
        uvicorn_process = run_uvicorn()

        # Tạo các thread để đọc đầu ra từ các tiến trình
        streamlit_thread_out = threading.Thread(target=read_output, args=(streamlit_process, "Streamlit"))
        streamlit_thread_err = threading.Thread(target=read_error, args=(streamlit_process, "Streamlit"))

        uvicorn_thread_out = threading.Thread(target=read_output, args=(uvicorn_process, "Uvicorn"))
        uvicorn_thread_err = threading.Thread(target=read_error, args=(uvicorn_process, "Uvicorn"))

        # Khởi động các thread
        streamlit_thread_out.start()
        streamlit_thread_err.start()
        uvicorn_thread_out.start()
        uvicorn_thread_err.start()

        print("Press Ctrl+C to stop the services...")

        # Đợi tiến trình kết thúc
        uvicorn_process.wait()

    except KeyboardInterrupt:
        print("Stopping services...")
        # Kết thúc các tiến trình khi người dùng nhấn Ctrl+C
        streamlit_process.terminate()
        uvicorn_process.terminate()

        # Đảm bảo các tiến trình được dừng hoàn toàn
        streamlit_process.wait()
        uvicorn_process.wait()

        print("Services stopped.")
