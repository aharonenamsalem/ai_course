import os
from dotenv import load_dotenv

load_dotenv()
openai = os.getenv("OPENAI_API_KEY")