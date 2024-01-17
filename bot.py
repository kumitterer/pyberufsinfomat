import random
import string
import html
import json
from urllib.request import Request, urlopen
from http.cookies import SimpleCookie

def get_token():
    url = 'https://berufsinfomat.prod.portal.ams.at/client/6453a57358480fb76ddc0a43/overlay'
    headers = {
        'User-Agent': ""
    }

    req = Request(url, headers=headers)
    res = urlopen(req)
    
    cookies = SimpleCookie()

    if 'Set-Cookie' in res.headers:
        cookie_headers = res.headers.get_all('Set-Cookie')
        for header in cookie_headers:
            cookies.load(header)

    return cookies["jwtToken"].value

def send_question_to_ams(question, chat_session_id, jwt_token):
    url = "https://berufsinfomat.prod.portal.ams.at/client/6453a57358480fb76ddc0a43/send_question"

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "",
        "Cookie": "jwtToken=" + jwt_token
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
    jwt_token = get_token()
    chat_session_id = "".join([random.SystemRandom().choice(string.hexdigits) for _ in range(32)])
    print("Welcome to the AMS Berufsinfomat interactive conversation!")
    print("Type 'exit' to end the conversation.\n")

    while True:
        question = input("> ")
        if question.lower() == "exit":
            print("Ending conversation.")
            break
        response = send_question_to_ams(question, chat_session_id, jwt_token)
        print(response + "\n")

if __name__ == "__main__":
    main()
