import requests
import os
import sys

BASE_URL = os.getenv("CANVAS_BASE_URL")
TOKEN = os.getenv("CANVAS_TOKEN")

HEADERS = {"Authorization": f"Bearer {TOKEN}"}

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
    found_new_quiz = False

    courses = get_courses()
    for course in courses:
        quizzes = get_quizzes(course["id"])
        for quiz in quizzes:
            if quiz.get("published"):
                print(f"NEW QUIZ: {course['name']} — {quiz['title']}")
                found_new_quiz = True

    if found_new_quiz:
        # Force GitHub Actions to send an email
        sys.exit("New Canvas quiz detected")

if __name__ == "__main__":
    main()
