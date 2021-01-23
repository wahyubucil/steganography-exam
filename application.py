import os
from flask import Flask, render_template, request, redirect, send_from_directory, send_file
from werkzeug.utils import secure_filename
from PIL import Image
from steganography import Steganography
from utils import allowed_file, filename_with_random_str

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024

if (not os.path.isdir(app.config['UPLOAD_FOLDER'])):
  os.mkdir(app.config['UPLOAD_FOLDER'])

@app.route('/')
def main():
  return render_template('main/index.html')

@app.route('/uploads/<filename>', methods=['GET', 'POST'])
def uploaded_file(filename):
  if request.method == 'POST':
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    return send_file(path, as_attachment=True)
    
  return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/encode', methods=['POST'])
def encode():
  if 'show_image' not in request.files or 'hide_image' not in request.files:
    return redirect('/')
  
  show_image = request.files['show_image']
  hide_image = request.files['hide_image']

  if show_image.filename == '' or hide_image.filename == '':
    return redirect('/')

  if (show_image and allowed_file(show_image.filename)) and (hide_image and allowed_file(hide_image.filename)):
    show_image_filename = secure_filename(show_image.filename)
    show_image_filename = filename_with_random_str(show_image_filename)
    show_image_path = os.path.join(app.config['UPLOAD_FOLDER'], show_image_filename)
    show_image.save(show_image_path)

    hide_image_filename = secure_filename(hide_image.filename)
    hide_image_filename = filename_with_random_str(hide_image_filename)
    hide_image_path = os.path.join(app.config['UPLOAD_FOLDER'], hide_image_filename)
    hide_image.save(hide_image_path)

    try:
      encoded_image = Steganography.encode(Image.open(show_image_path), Image.open(hide_image_path))
      encoded_image_filename = 'encoded_' + show_image_filename
      encoded_image_path = os.path.join(app.config['UPLOAD_FOLDER'], encoded_image_filename)
      encoded_image.save(encoded_image_path)

      return render_template('main/encode.html', filename=encoded_image_filename)
    except ValueError as e:
      return str(e)
  else:
    return 'Not allowed extensions'

@app.route('/decode', methods=['GET', 'POST'])
def decode():
  if request.method == 'POST':
    if 'image' not in request.files:
      return redirect(request.url)
    image = request.files['image']
    if image.filename == '':
      return redirect(request.url)
    if image and allowed_file(image.filename):
      image_filename = secure_filename(image.filename)
      image_filename = filename_with_random_str(image_filename)
      image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
      image.save(image_path)

      decoded_image = Steganography.decode(Image.open(image_path))
      decoded_image_filename = 'decoded_' + image_filename
      decoded_image_path = os.path.join(app.config['UPLOAD_FOLDER'], decoded_image_filename)
      decoded_image.save(decoded_image_path)

      return render_template('decode/show.html', filename=decoded_image_filename)
  
  return render_template('decode/index.html')
