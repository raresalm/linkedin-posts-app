import openai
import schedule
import time
from datetime import datetime

from dotenv import load_dotenv
import os

load_dotenv()  # Reads the .env file and loads the variables

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

if GITHUB_TOKEN is None:
    raise ValueError("GitHub token not found! Please create a .env file with GITHUB_TOKEN=your_token")


# Configuration
OPENAI_API_KEY = 'your_openai_api_key'
POSTING_TIMES = ["09:00", "14:00", "18:00"]  # Times to post daily

# Set up OpenAI API
openai.api_key = OPENAI_API_KEY

def generate_ai_content():
    prompt = "Generate a professional, insightful post on artificial intelligence trends for a tech-savvy audience. Include an engaging question at the end."
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=250
    )
    return response.choices[0].message['content'].strip()

def post_content():
    post_text = generate_ai_content()
    print(f"\n[{datetime.now()}] Generated Content:")
    print(post_text)
    # Save the content to a file for later use or manual posting
    with open("generated_posts.txt", "a", encoding="utf-8") as f:
        f.write(f"\n[{datetime.now()}]\n{post_text}\n")

# Schedule posts
for posting_time in POSTING_TIMES:
    schedule.every().day.at(posting_time).do(post_content)

print("AI Post Generator is running...")

while True:
    schedule.run_pending()
    time.sleep(60)
