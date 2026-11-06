
import os
import json
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

from dotenv import load_dotenv

project_root = Path(__file__).resolve().parents[2]
load_dotenv(project_root / ".env")

api_key = os.getenv("MISTRAL_API_KEY")

if not api_key:
    raise ValueError("MISTRAL_API_KEY bulunamadi.")

url = "https://api.mistral.ai/v1/chat/completions"

payload = {
    "model": "mistral-small-latest",
    "messages": [
        {
            "role": "user",
            "content": "Merhaba! Tek cumleyle kendini tanit."
        }
    ]
}

request = Request(
    url,
    data=json.dumps(payload).encode("utf-8"),
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    },
    method="POST"
)

print("Mistral API baglantisi test ediliyor...")

try:
    with urlopen(request, timeout=30) as response:
        result = json.loads(response.read().decode("utf-8"))

    print("\nMISTRAL YANITI:")
    print(result["choices"][0]["message"]["content"])
    print("\nAPI baglantisi basarili.")

except HTTPError as error:
    print(f"HTTP hatasi: {error.code}")
    print(error.read().decode("utf-8"))

except URLError as error:
    print(f"Baglanti hatasi: {error.reason}")
