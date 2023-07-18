import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests
from flask import Flask, render_template, request

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
    sender_email = my_email
    sender_password = password
    recipient_email = "szabo.gergo.bme@gmail.com"
    subject = "New blog message received"
    body = f"Name: {name}\nEmail: {email}\nPhone: {phone}\nMessage:{message}"

    message = MIMEMultipart()
    message['Subject'] = subject
    message['From'] = sender_email
    message['To'] = recipient_email
    html_part = MIMEText(body)
    message.attach(html_part)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, message.as_string())


@app.route('/post/<blog_id>')
def get_blog(blog_id):
    post_to_render = all_posts_json[int(blog_id) - 1]
    return render_template("post.html", post_to_render=post_to_render)


if __name__ == "__main__":
    app.run(debug=True)
