# Minor change to trigger Git
# Flask requirement
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'Welcome to Rhythm & Reality! 🚀'

if __name__ == '__main__':
    app.run(debug=True)