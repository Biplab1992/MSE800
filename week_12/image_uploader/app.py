import os
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        if file := request.files['image']:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            return render_template('index.html', filename=filename)
    return render_template('index.html', filename=None)

@app.route('/uploads/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename=f'uploads/{filename}'), code=301)

if __name__ == '__main__':
    app.run(debug=True)