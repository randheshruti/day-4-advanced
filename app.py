from flask import flash, redirect, url_for
from forms import RegistrationForm
from flask import Flask, render_template, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
from flask_sqlalchemy import SQLAlchemy
app.config["SECRET_KEY"] = "my-development-secret-key"

# Sample blog posts
posts = [
    {
        "id": 1,
        "title": "Introduction to Python",
        "content": "Python is a popular programming language. It is easy to learn and widely used in web development, data science and AI."
    },
    {
        "id": 2,
        "title": "What is Flask?",
        "content": "Flask is a lightweight Python web framework used to build web applications."
    },
    {
        "id": 3,
        "title": "Learning Jinja2",
        "content": "Jinja2 is a template engine that allows dynamic content to be displayed in HTML pages."
    }
]

@app.route("/")
@app.route("/add-samples")
def add_samples():
    if Post.query.count() == 0:
        post1 = Post(title="Introduction to Python", content="Python is a beginner-friendly programming language.")
        post2 = Post(title="What is Flask?", content="Flask is a lightweight Python web framework.")
        post3 = Post(title="Learning SQLite", content="SQLite is a lightweight database.")

        db.session.add_all([post1, post2, post3])
        db.session.commit()

    return "Sample posts added successfully!"
def home():
    posts = Post.query.all()
    return render_template("posts.html", posts=posts)
@app.route("/post/<int:post_id>")
def post_detail(post_id):
    post = db.session.get(Post, post_id)

    if post is None:
        abort(404)

    return render_template("post_detail.html", post=post)
    post = next((p for p in posts if p["id"] == post_id), None)

    if post is None:
        abort(404)

    return render_template("post_detail.html", post=post)
@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        flash("Registration successful!", "success")
        return redirect(url_for("home"))

    if form.is_submitted() and not form.validate():
        flash("Please correct the errors in the form.", "error")

    return render_template("register.html", form=form)
if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
