import random
import string
import html
import json
from urllib.request import Request, urlopen

def send_question_to_ams(question, chat_session_id):
    url = "https://berufsinfomat.prod.portal.ams.at/client/6453a57358480fb76ddc0a43/send_question"

    headers = {
        "Content-Type": "application/json",
        "User-Agent": ""
    }

    data = json.dumps({
        "question": question,
        "chat_session_id": chat_session_id
    }).encode("utf-8")

    req = Request(url, headers=headers, data=data)
    response = urlopen(req)

    text = html.unescape(response.read().decode()).replace("<br>", "\n").replace("<br/>", "\n").replace("<br />", "\n")
    return text.split("===")[-1].strip()

def main():
    chat_session_id = "".join([random.SystemRandom().choice(string.hexdigits) for _ in range(32)])
    print("Welcome to the AMS Berufsinfomat interactive conversation!")
    print("Type 'exit' to end the conversation.\n")

    while True:
        question = input("> ")
        if question.lower() == "exit":
            print("Ending conversation.")
            break
        response = send_question_to_ams(question, chat_session_id)
        print(response + "\n")

if __name__ == "__main__":
    main()