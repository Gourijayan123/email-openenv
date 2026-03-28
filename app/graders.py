from app.environment import EmailEnvironment

def run_grader(task_id: str, email_text: str) -> dict:
    """Run a single grader for a specific task."""
    env = EmailEnvironment()
    env.reset(task_id=task_id)
    result = env.step(email_text)
    return {
        "task_id": task_id,
        "score": result["score"],
        "feedback": result["feedback"],
    }


def grade_easy(email_text: str) -> dict:
    return run_grader("easy", email_text)


def grade_medium(email_text: str) -> dict:
    return run_grader("medium", email_text)


def grade_hard(email_text: str) -> dict:
    return run_grader("hard", email_text)


def run_all_graders(email_text: str) -> dict:
    """Run all 3 graders and return all scores."""
    return {
        "easy": grade_easy(email_text),
        "medium": grade_medium(email_text),
        "hard": grade_hard(email_text),
    }