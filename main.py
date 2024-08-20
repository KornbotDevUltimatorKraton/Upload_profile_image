from flask import Flask, request, render_template, jsonify, url_for
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
profile_image_path = "static/uploads/"
app.config['ALLOWED_IMAGE_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

def allowed_file_image(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_IMAGE_EXTENSIONS']

@app.route('/<accountdat>')
def index(accountdat):
    print("Account_data",accountdat)
    image_url = url_for('static', filename='uploads/'+accountdat+'/avatar.png') if os.path.exists('static/uploads/'+accountdat+'/avatar.png') else ''
    return render_template('index.html', image_url=image_url,account_email=accountdat)

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    email = request.form['email']
    print("Profile image of account : ",email,file.filename)
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    if file and allowed_file_image(file.filename):
        profile_image = os.listdir(profile_image_path)
        if email not in profile_image:
               try:
                   print("Create account directory data")
                   os.mkdir(profile_image_path+email)  
                   filename = secure_filename(file.filename)
                   file_path = os.path.join('static/uploads/'+email, 'avatar.png')
                   file.save(file_path)
                   return jsonify({'url': url_for('static', filename='uploads/'+email+'/avatar.png')})
               except:
                    print("Error creating the profile image")
                    return jsonify({'error': 'Invalid file type'})
        if email in profile_image:
                try:
                   filename = secure_filename(file.filename)
                   file_path = os.path.join('static/uploads/'+email, 'avatar.png')
                   file.save(file_path)
                   return jsonify({'url': url_for('static', filename='uploads/'+email+'/avatar.png')})
                except:
                    print("Error creating profile image ")              
                    return jsonify({'error': 'Invalid file type'})

if __name__ == '__main__':
    
    app.run(debug=True)
