from flask import Flask, render_template, Response
from camera_basler import Camera
from detection import Detect

app = Flask(__name__)

camera_basler = Camera()
detection = Detect()

@app.route("/")
def index():
    return render_template("index.html")

def read_from_webcam():
    while True:
        # Đọc ảnh từ class camera_basler
        image = next(camera_basler.get_img())

        # Nhận diện qua model yolov5
        image = detection.detect(image)

        # Trả về cho web bằng lệnh yeild
        yield b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n--frame\r\n'


@app.route("/image_feed")
def image_feed():
    return Response( read_from_webcam(), mimetype="multipart/x-mixed-replace; boundary=frame" )

if __name__=="__main__":
    app.run(host='0.0.0.0', debug=False)
