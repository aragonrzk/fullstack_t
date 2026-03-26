import os
from dotenv import load_dotenv

load_dotenv()

# Database Configuration
DATABASE_URL = "postgresql://aragon:masuk123@localhost:5432/pos_ku"

# Security Configuration
SECRET_KEY = os.environ.get('SECRET_KEY', 'pt_xyz_secret_key_2024_change_in_production')
WTF_CSRF_ENABLED = True
WTF_CSRF_TIME_LIMIT = 3600  # 1 hour

# Pagination Configuration
PER_PAGE_DEFAULT = 10
PER_PAGE_OPTIONS = [10, 25, 50, 100]
