from flask import Flask, render_template

app = Flask(__name__)

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
    app.run(debug=True)
