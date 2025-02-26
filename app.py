from flask import Flask, render_template, Response
import cv2
import threading

app = Flask(__name__)

# Initialize cameras
curfew_camera = cv2.VideoCapture(0)  # Adjust index if needed
fire_exit_camera = cv2.VideoCapture(1)  # Adjust index if needed
fence_camera = cv2.VideoCapture(2)  # Adjust index if needed

def generate_frames(camera):
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/curfew')
def curfew():
    return render_template('curfew.html')

@app.route('/fence')
def fence():
    return render_template('fence.html')

@app.route('/fire_exit')
def fire_exit():
    return render_template('fexit.html')

@app.route('/curfew_feed')
def curfew_feed():
    return Response(generate_frames(curfew_camera), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/fire_exit_feed')
def fire_exit_feed():
    return Response(generate_frames(fire_exit_camera), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/fence_feed')
def fence_feed():
    return Response(generate_frames(fence_camera), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
