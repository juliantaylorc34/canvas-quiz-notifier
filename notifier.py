import requests
import os

BASE_URL = os.getenv("CANVAS_BASE_URL")
TOKEN = os.getenv("CANVAS_TOKEN")

HEADERS = {"Authorization": f"Bearer {TOKEN}"}

def get_courses():
    r = requests.get(f"{BASE_URL}/api/v1/courses", headers=HEADERS)
    r.raise_for_status()
    return r.json()

def get_quizzes(course_id):
    url = f"{BASE_URL}/api/v1/courses/{course_id}/quizzes"
    r = requests.get(url, headers=HEADERS)

    if r.status_code == 404:
        # Course has no quizzes or quizzes are not accessible
        return []

    r.raise_for_status()
    return r.json()

def main():
    courses = get_courses()

    for course in courses:
        quizzes = get_quizzes(course["id"])
        for quiz in quizzes:
            if quiz.get("published"):
                print(f"Quiz available: {course['name']} — {quiz['title']}")

if __name__ == "__main__":
    main()
