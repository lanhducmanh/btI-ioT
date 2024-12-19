from flask import Flask
from sense_emu import SenseHat
import threading
import time

app = Flask(__name__)
sense = SenseHat()

# Flask route để lấy dữ liệu sensor
@app.route('/ducmanh')
def get_sensor_data():
    temperature = sense.get_temperature()
    humidity = sense.get_humidity()
    pressure = sense.get_pressure()
    return (f"Temperature: {temperature:.2f} °C, "
            f"Humidity: {humidity:.2f} %, "
            f"Pressure: {pressure:.2f} hPa")

# Hàm hiển thị dữ liệu trên Sense HAT
def display_sensor_data():
    while True:
        temperature = sense.get_temperature()
        humidity = sense.get_humidity()
        pressure = sense.get_pressure()
        # Hiển thị nhiệt độ, độ ẩm, áp suất trên LED ma trận của Sense HAT
        sense.show_message(
            f"T:{temperature:.1f}C H:{humidity:.1f}% P:{pressure:.1f}hPa",
            scroll_speed=0.05,
            text_colour=[0, 255, 0]
        )
        time.sleep(2)  # Đợi 2 giây trước khi cập nhật

# Chạy Flask và hiển thị Sense HAT đồng thời
if __name__ == '__main__':
    # Tạo một luồng riêng để hiển thị Sense HAT
    display_thread = threading.Thread(target=display_sensor_data, daemon=True)
    display_thread.start()
    
    # Chạy Flask trên host và port cụ thể
    app.run(host='0.0.0.0', port=6108)
