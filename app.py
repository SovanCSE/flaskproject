from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
##[DB_TYPE]+[DB_CONNECTOR]://[USERNAME]:[PASSWORD]@[HOST]:[PORT]/[DB_NAME]
##mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@localhost:3306/{DB_NAME}
app.config['SECRET_KEY'] = 'shhhh...iAmASecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://uosztxa52ysc0hlu:tqhCzBdmdSzokLN3duDF@bru4mbyoptuuwmzoxgjr-mysql.services.clever-cloud.com:3306/bru4mbyoptuuwmzoxgjr'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title= db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False, default='N/A')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return "Blog post {}".format(self.id)

# all_posts = [
#     {
#      "title": "Post1",
#      "content": "This is content for first post 1 lalalalala",
#      "author": "sovan"
#     },
#     {
#      "title":"Post2",
#      "content": "This is content for first post 2 HaHaHAHa"
#     }
# ]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/posts', methods=['GET', 'POST'])
def posts():
    if request.method == "POST":
        title = request.form.get('title','')
        content=request.form.get('content', '')
        author=request.form.get('author','')
        new_post = BlogPost(title=title, content=content, author=author if author else 'N/A')
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        all_posts = BlogPost.query.order_by(BlogPost.date_posted.desc()).all()
        return render_template('posts.html', posts=all_posts)

@app.route('/post/edit/<int:id>', methods=['GET', 'POST'])
def edit_post(id):
    post = BlogPost.query.get_or_404(id)
    if request.method == "POST":
        post.title = request.form.get('title', '')
        post.content = request.form.get('content', '')
        post.author = request.form.get('author', '')
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.html', post=post)

@app.route('/post/delete/<int:id>')
def delete_post(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')

if __name__ == "__main__":
    app.run(debug=True)
