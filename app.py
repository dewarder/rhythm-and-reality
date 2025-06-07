from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
import os

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.jinja_env.auto_reload = True
app.secret_key = 'your_secret_key'

# Configure upload folder for music
UPLOAD_FOLDER = 'static/uploads/music'
ALLOWED_EXTENSIONS = {'mp3'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create upload directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Routes

@app.route('/')
def home():
    print("✅ Loading index.html...")
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route('/music', methods=["GET"])
def music():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template("music.html", files=files)

@app.route("/upload-music", methods=["POST"])
def upload_music():
    if 'file' not in request.files:
        flash('No file part in request')
        return redirect(url_for('music'))

    file = request.files['file']

    if file.filename == '':
        flash('No file selected')
        return redirect(url_for('music'))

    if file and allowed_file(file.filename):
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        flash('File uploaded successfully!')
    else:
        flash('Invalid file type. Only .mp3 files are allowed.')

    return redirect(url_for('music'))

@app.route('/uploads/music/<filename>')
def uploaded_music(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        story = request.form['story']
        links = request.form['links']
        why = request.form['why']

        print(f"New submission from {name}: {email}, {story}, {links}, {why}")
        flash('Thank you for your submission!')
        return redirect(url_for('thank_you', name=name))
    
    return render_template("submit.html")

@app.route('/thank-you')
def thank_you():
    name = request.args.get('name', 'Artist')
    return render_template("thankyou.html", name=name)

# ✅ Start the app
if __name__ == '__main__':
    app.run(debug=True)