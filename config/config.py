import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///compounds.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'txt', 'csv', 'jdx', 'dx', 'bin', 'dat', 'raw', 'spc', 'bz2', 'gz', 'zip', 'tar', 'h5', 'hdf5', 'npz', 'npy', 'mat', 'xlsx', 'xls', 'docx', 'doc', 'ppt', 'pptx', 'fid', 'log', 'propcar', 'text'}