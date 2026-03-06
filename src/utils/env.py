import os
from dotenv import load_dotenv

load_dotenv()  # reads .env from project root

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
OMDB_API_KEY = os.getenv("OMDB_API_KEY")

if not TMDB_API_KEY:
    raise ValueError("TMDB_API_KEY not found. Add it to your .env file.")
if not OMDB_API_KEY:
    raise ValueError("OMDB_API_KEY not found. Add it to your .env file.")