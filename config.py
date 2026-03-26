import os
from dotenv import load_dotenv

load_dotenv()

# Database config
# hilangkan tanda "[]"
DATABASE_URL = "postgresql://[user]:[password]@localhost:5432/[nama database]"

# Security config
SECRET_KEY = os.environ.get('SECRET_KEY', 'pt_xyz_secret_key_2024_change_in_production')
WTF_CSRF_ENABLED = True
WTF_CSRF_TIME_LIMIT = 3600  

# Pagination config
PER_PAGE_DEFAULT = 10
PER_PAGE_OPTIONS = [10, 25, 50, 100]
