import os

import requests
from flask import Flask, send_file, Response
from bs4 import BeautifulSoup

"""
https://canvas.uw.edu/courses/1206699/assignments/4315243?module_item_id=8562814
The requirement is:

1. You should deploy your assignment to Heroku.
2. Whenever someone visits your home page, it should scrape a new fact from unkno.com, send that fact to the pig latin website, and print out the address for the "pig latinized" text.

If you'd like to be fancy, then you can print the address as a clickable link.
"""

app = Flask(__name__)

listenAddress = ["0.0.0.0", "127.0.0.1"]  # quick configure for localhost
pigLatinSite = "https://hidden-journey-62459.herokuapp.com/"


def get_fact():
    """get facts from the unkno.com website"""

    response = requests.get("http://unkno.com")

    soup = BeautifulSoup(response.content, "html.parser")
    facts = soup.find_all("div", id="content")

    return facts[0].getText().strip()


def request_pig_latin_link(**kwargs):
    """Request piglatin transform from piglatinizer site."""

    input_text = kwargs["input_text"]

    res2 = requests.post(
        pigLatinSite + "piglatinize/",
        data={"input_text": input_text.lower()},
        allow_redirects="false",
    )

    return res2.url


def format_pig_latin_link(link=pigLatinSite):
    """Format the output from a link into a clickable href anchor"""

    a_href = "<a href=" + link + ">" + link + "</a>"
    page_open = "<html><title>Pig Latin Link</title><body>"
    content = page_open + "<p>" + link + "<p>" + a_href
    page_close = "</body></html>"
    page = page_open + content + page_close

    return page


def request_actual_piglatin(**kwargs):
    """Request piglatin transform from piglatinizer site.

    depreciated in favor of url linking code"""

    input_text = kwargs["input_text"]

    res2 = requests.post(
        pigLatinSite + "piglatinize/",
        data={"input_text": input_text.lower()},
        allow_redirects="false",
    )
    soup = BeautifulSoup(res2.content, "html.parser")
    return soup.get_text().strip()[37:].capitalize()


@app.route("/")
def home():
    input_text = get_fact()
    requested_link = request_pig_latin_link(input_text=input_text)

    return format_pig_latin_link(link=requested_link)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6787))
    app.run(host=listenAddress[0], port=port)
