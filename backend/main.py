from client import client_rec
from flask import Flask, render_template, Response


app = Flask(__name__, static_folder='./static')



@app.route('/')
def home():
      return render_template('home.html')

@app.route('/stream')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(client_rec(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True)