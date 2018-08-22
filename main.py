import os

import requests
from flask import Flask, send_file, Response
from bs4 import BeautifulSoup

app = Flask(__name__)

listenAddress = ["0.0.0.0", "127.0.0.1"]


def get_fact():

    response = requests.get("http://unkno.com")

    soup = BeautifulSoup(response.content, "html.parser")
    facts = soup.find_all("div", id="content")

    return facts[0].getText().strip()


@app.route("/")
def home():
    # return "FILL ME!"
    return get_fact()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6787))
    app.run(host=listenAddress[1], port=port)
