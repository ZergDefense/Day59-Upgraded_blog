import os
import smtplib

import requests
from flask import Flask, render_template, url_for, request

app = Flask(__name__)
api_endpoint = "https://api.npoint.io/6da3bd5b6bb70128aca2"
my_email = os.environ["EMAIL"]
password = os.environ["PASS"]

all_posts_json = requests.get(url=api_endpoint).json()


@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=all_posts_json)


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/form-entry', methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        data = request.form
        send_email(data["name"], data["email"], data["phone"], data["message"])
        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)


def send_email(name, email, phone, message):
    with smtplib.SMTP_SSL("smtp.gmail.com") as connection:
        connection.login(user=my_email, password=password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs="szabo.gergo.bme@gmail.com",
            msg=f"Subject:New blog message received\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage:{message}")


@app.route('/post/<blog_id>')
def get_blog(blog_id):
    post_to_render = all_posts_json[int(blog_id) - 1]
    return render_template("post.html", post_to_render=post_to_render)


if __name__ == "__main__":
    app.run(debug=True)
