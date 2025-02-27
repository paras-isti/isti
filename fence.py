import cv2
from flask import Blueprint, render_template, Response, jsonify

fence_bp = Blueprint('fence_bp', __name__)

camera = cv2.VideoCapture(0)
intruder_detected = False

# Adjusted bounding box for fence detection
ROI_X, ROI_Y, ROI_WIDTH, ROI_HEIGHT = 150, 50, 400, 200  # Change this for fence position

def generate_frames():
    global intruder_detected
    while True:
        success, frame = camera.read()
        if not success:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        roi = blurred[ROI_Y:ROI_Y + ROI_HEIGHT, ROI_X:ROI_X + ROI_WIDTH]
        edges = cv2.Canny(roi, 50, 150)

        detected = any(cv2.contourArea(c) > 500 for c in cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0])
        intruder_detected = detected

        color = (0, 0, 255) if intruder_detected else (0, 255, 0)
        cv2.rectangle(frame, (ROI_X, ROI_Y), (ROI_X + ROI_WIDTH, ROI_Y + ROI_HEIGHT), color, 3)

        _, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@fence_bp.route('/fence')
def fence():
    return render_template('fence.html')

@fence_bp.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@fence_bp.route('/alert-status')
def alert_status():
    return jsonify({'intruder': intruder_detected})
