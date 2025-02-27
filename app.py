from flask import Flask, render_template, redirect
from fexit import fexit_bp  # Import the blueprint
from fence import fence_bp  # Import fence blueprint

app = Flask(__name__)

app.register_blueprint(fence_bp)  # Register fence detection
app.register_blueprint(fexit_bp)  # Register the blueprint

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/curfew')
def curfew():
    return render_template('curfew.html')

@app.route('/fence')
def fence():
    return render_template('fence.html')

@app.route('/fexit')
def fexit():
    return render_template('fexit.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
