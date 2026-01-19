import requests
import os
import json
from pathlib import Path

BASE_URL = os.getenv("CANVAS_BASE_URL")
TOKEN = os.getenv("CANVAS_TOKEN")

TG_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TG_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

HEADERS = {"Authorization": f"Bearer {TOKEN}"}
SEEN_FILE = Path("seen_quizzes.json")


def send_telegram(message: str):
    if not TG_TOKEN or not TG_CHAT_ID:
        return
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": TG_CHAT_ID,
        "text": message
    })


def load_seen():
    if SEEN_FILE.exists():
        return set(json.loads(SEEN_FILE.read_text()))
    return set()


def save_seen(seen):
    SEEN_FILE.write_text(json.dumps(list(seen)))


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
    seen = load_seen()
    new_messages = []

    for course in get_courses():
        for quiz in get_quizzes(course["id"]):
            quiz_id = quiz.get("id")
            if quiz.get("published") and quiz_id not in seen:
                seen.add(quiz_id)
                new_messages.append(
                    f"📢 *New Canvas Quiz*\n"
                    f"Course: {course['name']}\n"
                    f"Quiz: {quiz['title']}"
                )

    if new_messages:
        send_telegram("\n\n".join(new_messages))
        print("Telegram notification sent")

    save_seen(seen)


if __name__ == "__main__":
    main()
