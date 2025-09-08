import os

# Railway deployment configuration

# Railway automatically provides these environment variables
DATABASE_URL = os.getenv("DATABASE_URL")
PORT = os.getenv("PORT", "8000")
HOST = os.getenv("HOST", "0.0.0.0")

# Update your config.py to use Railway's DATABASE_URL