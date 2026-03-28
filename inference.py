import os
from openai import OpenAI
import requests

API_BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:8000")
MODEL_NAME = os.environ.get("MODEL_NAME", "gpt-3.5-turbo")
HF_TOKEN = os.environ.get("HF_TOKEN", "")

client = OpenAI(
    base_url=API_BASE_URL,
    api_key=HF_TOKEN if HF_TOKEN else "dummy",
)

def ask_llm(situation: str) -> str:
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a professional email writer."},
            {"role": "user", "content": f"Situation: {situation}\n\nWrite a professional email for this situation."}
        ],
        max_tokens=300,
    )
    return response.choices[0].message.content

def run_inference():
    env_url = "http://localhost:8000"
    task_ids = ["easy", "medium", "hard"]
    total_score = 0.0

    print("=" * 50)
    print("Running Email OpenEnv Inference")
    print("=" * 50)

    for task_id in task_ids:
        reset_response = requests.post(f"{env_url}/reset", json={"task_id": task_id})
        task = reset_response.json()
        situation = task["situation"]

        print(f"\nTask: {task_id.upper()}")
        print(f"Situation: {situation}")

        email = ask_llm(situation)
        print(f"Generated Email:\n{email}")

        step_response = requests.post(f"{env_url}/step", json={"action": email})
        result = step_response.json()
        score = result["score"]
        total_score += score

        print(f"Score: {score}")
        print(f"Feedback: {result['feedback']}")
        print("-" * 50)

    avg_score = total_score / len(task_ids)
    print(f"\nFinal Average Score: {avg_score:.2f}")
    return avg_score

if __name__ == "__main__":
    run_inference()