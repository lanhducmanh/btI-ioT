from flask import Flask, jsonify
from sense_emu import SenseHat
import threading
import time
import sqlite3
import firebase_admin
from firebase_admin import credentials, db

# Khởi tạo Flask và Sense HAT
app = Flask(__name__)
sense = SenseHat()

# Khởi tạo Firebase
cred = credentials.Certificate("path/to/firebase_credentials.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://your-firebase-project.firebaseio.com/'
})

# Cấu hình SQLite
DB_NAME = "sensor_data.db"
conn = sqlite3.connect(DB_NAME, check_same_thread=False)
cursor = conn.cursor()

# Tạo bảng trong SQLite nếu chưa có
cursor.execute("""
CREATE TABLE IF NOT EXISTS temperature_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    temperature REAL
)
""")
conn.commit()

# Tham số lịch sử n
n = 5
t_history = []  # Danh sách để lưu lịch sử nhiệt độ

def calculate_t_loc(t, n):
    """Tính toán nhiệt độ lọc t_loc dựa trên trung bình của n giá trị lịch sử."""
    t_history.append(t)
    if len(t_history) > n:
        t_history.pop(0)
    return sum(t_history) / len(t_history)

def read_and_process_sensor_data():
    """Đọc dữ liệu từ Sense HAT, lưu vào SQLite, và gửi lên Firebase."""
    while True:
        t = sense.get_temperature()
        t_loc = calculate_t_loc(t, n)
        
        # Lưu vào SQLite
        cursor.execute("INSERT INTO temperature_data (temperature) VALUES (?)", (t,))
        conn.commit()
        
        # Gửi lên Firebase
        db.reference('temperature_data').set({
            'filtered_temperature': t_loc
        })
        
        print(f"Temperature: {t:.2f}, Filtered: {t_loc:.2f}")
        time.sleep(2)  # Đọc dữ liệu mỗi 2 giây

@app.route('/data')
def get_filtered_temperature():
    """API Flask để trả về dữ liệu nhiệt độ đã lọc."""
    ref = db.reference('temperature_data')
    data = ref.get()
    return jsonify(data)

# Chạy Flask và xử lý dữ liệu đồng thời
if __name__ == '__main__':
    # Tạo một luồng riêng để đọc và xử lý dữ liệu
    sensor_thread = threading.Thread(target=read_and_process_sensor_data, daemon=True)
    sensor_thread.start()

    # Chạy Flask
    app.run(host='0.0.0.0', port=5000)