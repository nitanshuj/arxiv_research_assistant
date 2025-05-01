from dotenv import load_dotenv
import os
import time

def load_env_vars():
    load_dotenv()
    
def save_feedback(feedback: str):
    os.makedirs("./static/feedback", exist_ok=True)
    timestamp = int(time.time())
    with open(f"./static/feedback/feedback_{timestamp}.txt", "w") as f:
        f.write(feedback)