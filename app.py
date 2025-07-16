from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Basic Auth
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    auth = request.authorization
    if not auth or not (auth.username == ADMIN_USERNAME and auth.password == ADMIN_PASSWORD):
        return "Unauthorized", 401

    if request.method == 'POST':
        category = request.form['category']
        files = request.files.getlist('files')
        saved = 0

        cat_folder = os.path.join(app.config['UPLOAD_FOLDER'], category.lower())
        os.makedirs(cat_folder, exist_ok=True)

        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(cat_folder, filename))
                saved += 1
        return f"{saved} files uploaded to {category}"

    return '''
        <form method="post" enctype="multipart/form-data">
            Category: <input name="category" required><br>
            Upload images: <input type="file" name="files" multiple required><br>
            <input type="submit" value="Upload">
        </form>
    '''

if __name__ == '__main__':
    app.run(debug=True)