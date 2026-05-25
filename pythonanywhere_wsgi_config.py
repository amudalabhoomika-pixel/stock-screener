# PythonAnywhere WSGI Configuration
# 
# Usage:
# 1. In PythonAnywhere Web tab
# 2. Find "WSGI configuration file"
# 3. Click to edit
# 4. Replace content with this file (update YOUR_USERNAME)
# 5. Save
# 6. Click Reload button

import sys
import os

# Add your project directory to path
path = '/home/YOUR_USERNAME/stock-screener'
if path not in sys.path:
    sys.path.append(path)

# Set working directory
os.chdir(path)

# Load environment variables from .env
from dotenv import load_dotenv
load_dotenv('/home/YOUR_USERNAME/stock-screener/.env')

# Import Flask app
from app import app as application
