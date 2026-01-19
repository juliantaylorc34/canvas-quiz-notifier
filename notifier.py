import requests
import os
import sys

BASE_URL = os.getenv("CANVAS_BASE_URL")
TOKEN = os.getenv("CANVAS_TOKEN")

TG_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TG_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

HEADERS = {"Authorization": f"Bearer {TOKEN}"}

def send_telegram(msg: str):
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": TG_CHAT_ID,
        "text": msg
    })

def get_courses():
    r = requests.get(f"{BASE_URL}/api/v1/courses", headers=HEADERS)
    r.raise_for_status()
    return r.json()

def get_quizzes(course_id):
    r = requests.get(
        f"{BASE_URL}/api/v1/courses/{course_id}/quizzes",
        headers=HEADERS
    )
    if r.status_code == 404:
        return []
    r.raise_for_status()
    return r.json()

def main():
    courses = get_courses()
    messages = []

    for course in courses:
        quizzes = get_quizzes(course["id"])
        for quiz in quizzes:
            if quiz.get("published"):
                messages.append(
                    f"📢 New Canvas quiz\n"
                    f"Course: {course['name']}\n"
                    f"Quiz: {quiz['title']}"
                )

    if messages:
        send_telegram("\n\n".join(messages))
        sys.exit("New Canvas quiz detected")

if __name__ == "__main__":
    main()
