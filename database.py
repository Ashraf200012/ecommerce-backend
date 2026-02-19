import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load the secret keys from the .env file
load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

# Create the connection to Supabase
supabase: Client = create_client(url, key)