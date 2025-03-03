import cv2
from flask import Blueprint, render_template, Response, jsonify

curfew_bp = Blueprint('curfew_bp', __name__)

person_detected = False

# Define ROI for Curfew
ROI_X, ROI_Y, ROI_WIDTH, ROI_HEIGHT = 0, 0, 635, 475  # Curfew ROI

def generate_frames():
    global person_detected
    camera = cv2.VideoCapture(0)  # Create a separate camera instance

    while True:
        success, frame = camera.read()
        if not success:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        roi = blurred[ROI_Y:ROI_Y + ROI_HEIGHT, ROI_X:ROI_X + ROI_WIDTH]
        edges = cv2.Canny(roi, 50, 150)

        detected = any(cv2.contourArea(c) > 500 for c in cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0])
        obstruction_detected = detected

        color = (0, 0, 255) if obstruction_detected else (0, 255, 0)
        cv2.rectangle(frame, (ROI_X, ROI_Y), (ROI_X + ROI_WIDTH, ROI_Y + ROI_HEIGHT), color, 3)

        _, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

    camera.release()  # Release camera when done

@curfew_bp.route('/curfew')
def curfew():
    return render_template('curfew.html')

@curfew_bp.route('/curfew/video_feed')
def curfew_video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@curfew_bp.route('/alert-status')
def alert_status():
    return jsonify({'person': person_detected})