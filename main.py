import requests
from flask import Flask, render_template, url_for

app = Flask(__name__)
api_endpoint = "https://api.npoint.io/6da3bd5b6bb70128aca2"

all_posts_json = requests.get(url=api_endpoint).json()


@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=all_posts_json)


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/contact')
def contact():
    return render_template("contact.html")


@app.route('/post/<blog_id>')
def get_blog(blog_id):
    post_to_render = all_posts_json[int(blog_id) - 1]
    return render_template("post.html", post_to_render=post_to_render)


if __name__ == "__main__":
    app.run(debug=True)
