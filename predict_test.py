import requests

url = 'http://localhost:9696/check'

tests = [
    "URGENT! You have won a 1 week FREE membership. Call now!",
    "Hey, are we still meeting for lunch tomorrow?",
    "Your account has been suspended. Verify your details immediately.",
    "Can you send me the report by 5pm?",
]

for text in tests:
    response = requests.post(url, json={"text": text}).json()
    print(f"{text[:50]}... → {response}")