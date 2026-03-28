import random
from typing import Optional

TASKS = [
    {
        "id": "easy",
        "level": "easy",
        "situation": "You received a gift from your colleague. Write a short thank-you email to them.",
        "required_keywords": ["thank", "grateful", "appreciate"],
        "min_words": 20,
        "max_words": 100,
    },
    {
        "id": "medium",
        "level": "medium",
        "situation": "You missed an important meeting with your manager. Write an apology email and suggest a solution.",
        "required_keywords": ["sorry", "apolog", "reschedule"],
        "min_words": 40,
        "max_words": 150,
    },
    {
        "id": "hard",
        "level": "hard",
        "situation": "A vendor has failed to deliver your order for the third time. Write a professional complaint email escalating the issue to their manager.",
        "required_keywords": ["disappointed", "unacceptable", "immediate", "resolv"],
        "min_words": 60,
        "max_words": 200,
    },
]


class EmailEnvironment:
    def __init__(self):
        self.current_task = None
        self.current_email = None
        self.is_done = False

    def reset(self, task_id: Optional[str] = None):
        self.is_done = False
        self.current_email = None

        if task_id:
            task = next((t for t in TASKS if t["id"] == task_id), None)
            if not task:
                task = random.choice(TASKS)
        else:
            task = random.choice(TASKS)

        self.current_task = task

        return {
            "task_id": task["id"],
            "level": task["level"],
            "situation": task["situation"],
            "instructions": "Write a professional email responding to the situation above.",
        }

    def step(self, action: str):
        if not self.current_task:
            return {"error": "Call reset() first to start a task."}

        self.current_email = action
        self.is_done = True
        score, feedback = self._score_email(action, self.current_task)

        return {
            "score": score,
            "feedback": feedback,
            "done": True,
        }

    def state(self):
        return {
            "task": self.current_task,
            "submitted_email": self.current_email,
            "is_done": self.is_done,
        }

    def _score_email(self, email: str, task: dict) -> tuple:
        score = 0.0
        feedback = []
        words = email.lower().split()
        word_count = len(words)

        if word_count >= task["min_words"]:
            score += 0.2
        else:
            feedback.append(f"Too short. Write at least {task['min_words']} words.")

        greetings = ["dear", "hello", "hi", "good morning", "good afternoon"]
        if any(g in email.lower() for g in greetings):
            score += 0.2
        else:
            feedback.append("Missing a greeting (e.g. 'Dear...' or 'Hello...')")

        signoffs = ["regards", "sincerely", "thank you", "best", "yours"]
        if any(s in email.lower() for s in signoffs):
            score += 0.2
        else:
            feedback.append("Missing a sign-off (e.g. 'Regards,' or 'Sincerely,')")

        keyword_score = 0.0
        for keyword in task["required_keywords"]:
            if keyword in email.lower():
                keyword_score += 1.0
        keyword_ratio = keyword_score / len(task["required_keywords"])
        score += keyword_ratio * 0.4

        if keyword_ratio < 1.0:
            feedback.append("Missing some key content for this task type.")

        if score >= 0.8:
            feedback.append("Great email!")
        elif score >= 0.5:
            feedback.append("Decent email, but needs improvement.")
        else:
            feedback.append("Email needs significant improvement.")

        return round(score, 2), feedback
    