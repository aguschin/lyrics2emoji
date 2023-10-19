import decouple  # pip install python-decouple
import requests


API_ENDPOINT = "https://api.openai.com/v1/chat/completions"
API_KEY = decouple.config("OPENAI_API_KEY")
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}


def get_prompt(song):
    return (
        f"<s>[INST] "
        f"You're an excellent translator from text to emoji. "
        f"You know how to replace word with emoji, keeping the meaning ideally. "
        f"Read this text. rgeturn it back, but replace each word with emoji . "
        f"Your output should contain emojis only. "
        f"Ensure that you have only emojis in your output and don't have any alphabet characters. "
        f"Text:\n"
        f"{song}"
        f"\n"
        f"[/INST]"
    )


def translate_text(text):
    if not text:
        return text
    data = {
        "model": "gpt-4",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": get_prompt(text)},
        ],
        "temperature": 0.3,
    }

    response = requests.post(API_ENDPOINT, json=data, headers=headers)

    if response.status_code == 200:
        result = response.json()
        return result["choices"][0]["message"]["content"]
    else:
        print(f"Error: {response.status_code} - {response.text}")

    return None


if __name__ == "__main__":
    print("Usage:")
    print("from chatgpt.text_to_emoji import translate_text")
    print("translate_text(TXT)")
    print()
    print("Can you guess the song?")
    song = """
    I was five and he was six
    We rode on horses made of sticks
    He wore black and I wore white
    He would always win the fight
    """
    print(translate_text(song))
