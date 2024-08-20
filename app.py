from flask import Flask, request, render_template, jsonify, url_for
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/<email_account>')
def index(email_account):
    #account_email = request.args.get('email', '')
    #jwt decode may be 
    image_url = url_for('static', filename=f'uploads/'+email_account+'/avatar.jpg') if email_account and os.path.exists(f'static/uploads/'+email_account+'/avatar.jpg') else ''
    return render_template('index2.html', account_email=email_account, image_url=image_url)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files or 'email' not in request.form:
        return jsonify({'error': 'No file part or email provided'})
    
    file = request.files['file']
    email = request.form['email']
    
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type or no selected file'})
    
    # Create a secure directory path using the email
    email_directory = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(email))
    if not os.path.exists(email_directory):
        os.makedirs(email_directory)

    # Save the file as avatar.jpg in the email directory
    file_path = os.path.join(email_directory, 'avatar.jpg')
    file.save(file_path)
    
    return jsonify({'url': url_for('static', filename=f'uploads/{email}/avatar.jpg')})

if __name__ == '__main__':
    app.run(debug=True)
