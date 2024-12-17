\\ Viết mã nguồn Flask**

from flask import Flask, render_template
from sense_emu import SenseHat

app = Flask(__name__)
sense = SenseHat()

@app.route("/")
def index():
    temperature = round(sense.get_temperature(), 1)
    humidity = round(sense.get_humidity(), 1)
    pressure = round(sense.get_pressure(), 1)

    joystick_event = sense.stick.get_events()
    joystick_x, joystick_y = 0, 0

    for event in joystick_event:
        if event.action == "pressed":
            if event.direction == "up":
                joystick_y -= 1
            elif event.direction == "down":
                joystick_y += 1
            elif event.direction == "left":
                joystick_x -= 1
            elif event.direction == "right":
                joystick_x += 1

    return render_template("dashboard.html",
                           temperature=temperature,
                           humidity=humidity,
                           pressure=pressure,
                           joystick_x=joystick_x,
                           joystick_y=joystick_y)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)

//khoi tao html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SenseHat Dashboard</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            margin-top: 30px;
        }
        .led-matrix {
            width: 50px;
            height: 50px;
            background-color: black;
            margin: 20px auto;
        }
        .led-dot {
            width: 10px;
            height: 10px;
            background-color: green;
            margin: auto;
        }
    </style>
</head>
<body>
    <h1>SenseHat Dashboard</h1>
    <h3>Thông tin môi trường</h3>
    <p>Nhiệt độ: {{ temperature }} °C</p>
    <p>Độ ẩm: {{ humidity }} %</p>
    <p>Áp suất: {{ pressure }} hPa</p>

    <h3>Trạng thái Joystick</h3>
    <p>Tọa độ joystick: x={{ joystick_x }}, y={{ joystick_y }}</p>

    <h3>LED Matrix</h3>
    <div class="led-matrix">
        <div class="led-dot"></div>
    </div>
</body>
</html>

// chay chuong trinh

python3 app.py

