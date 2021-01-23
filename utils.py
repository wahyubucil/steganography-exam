import string
import secrets

def allowed_file(filename: str) -> bool:
  allowed_extensions = {'tiff', 'bmp', 'png', 'jpg', 'jpeg', 'gif'}
  return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def random_str(size = 6, chars = string.ascii_lowercase + string.digits) -> str:
  return ''.join(secrets.choice(chars) for _ in range(size))

def filename_with_random_str(filename: str) -> str:
  filename = filename.rsplit('.', 1)
  random = random_str()
  return filename[0] + '_' + random + '.' + filename[1]