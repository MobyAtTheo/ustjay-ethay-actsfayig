import os

import requests
from flask import Flask, send_file, Response
from bs4 import BeautifulSoup

app = Flask(__name__)

listenAddress = ["0.0.0.0", "127.0.0.1"]

pigLatinSite = "https://hidden-journey-62459.herokuapp.com/"


def get_fact():

    response = requests.get("http://unkno.com")

    soup = BeautifulSoup(response.content, "html.parser")
    facts = soup.find_all("div", id="content")

    return facts[0].getText().strip()


def request_pig_latin(**kwargs):
    """Request piglatin transform from piglatinizer site."""

    input_text = kwargs["input_text"]

    res2 = requests.post(
        pigLatinSite + "piglatinize/", data={"input_text": input_text.lower()}
    )
    soup = BeautifulSoup(res2.content, "html.parser")

    return soup.get_text().strip()[37:].capitalize()


@app.route("/")
def home():
    # return "FILL ME!"
    # return get_fact()
    return request_pig_latin(input_text="thisisatest")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6787))
    app.run(host=listenAddress[1], port=port)
