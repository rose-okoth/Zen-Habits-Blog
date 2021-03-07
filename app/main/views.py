from flask import render_template,request,redirect,url_for,abort,flash
from . import main
from ..models import User,Blog,Comment,Subscriber
from .. import db,photos
from .forms import UpdateProfile,BlogForm,CommentForm
from flask_login import login_required,current_user
from ..request import get_quotes
import datetime
from ..email import mail_message

# Views

@main.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''

    title = 'Zen Blog'

    # Getting reviews by category
    technology_blogs = Blog.get_blogs('technology')
    books_blogs = Blog.get_blogs('books')
    entertainment_blogs = Blog.get_blogs('entertainment')
    quotes = get_quotes()
    return render_template('index.html',title = title, technology = technology_blogs, books = books_blogs, entertainment = entertainment_blogs, quote = quotes)

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()
    blogs_count = Blog.count_blogs(uname)
    user_joined = user.date_joined.strftime('%b %d, %Y')

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user,blogs = blogs_count,date = user_joined)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form = form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))

@main.route('/blog/new', methods = ['GET','POST'])
@login_required
def new_blog():
    subscribers = Subscriber.query.all()
    blog_form = BlogForm()
    if blog_form.validate_on_submit():
        title = blog_form.title.data
        blog = blog_form.text.data
        category = blog_form.category.data
        user_id =  current_user._get_current_object().id

        # Updated blog instance
        new_blog = Blog(blog_title=title,blog_content=blog,category=category,user=current_user)

        # Save blog method
        new_blog.save_blog()
        for subscriber in subscribers:
            mail_message("New Blog Post","email/new_blog",subscriber.email,new_blog=new_blog)
        return redirect(url_for('.index'))
        flash('You Posted a new Blog')

    title = 'New blog'
    return render_template('create_post.html',title = title,blog_form=blog_form )

@main.route('/blogs/technology_blogs')
def technology_blogs():

    blogs = Blog.get_blogs('technology')

    return render_template("technology_blogs.html", blogs = blogs)

@main.route('/blogs/books_blogs')
def books_blogs():

    blogs = Blog.get_blogs('books')

    return render_template("books_blogs.html", blogs = blogs)

@main.route('/blogs/entertainment_blogs')
def entertainment_blogs():

    blogs = Blog.get_blogs('entertainment')

    return render_template("entertainment_blogs.html", blogs = blogs)


@main.route('/blog/<int:id>', methods = ['GET','POST'])
def blog(id):
    blog = Blog.get_blog(id)
    posted_date = blog.posted.strftime('%b %d, %Y')

    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        comment = comment_form.text.data

        new_comment = Comment(comment = comment,user = current_user,blog_id = blog)

        new_comment.save_comment()


    comments = Comment.get_comments(blog)

    return render_template("blog.html", blog = blog, comment_form = comment_form, comments = comments, date = posted_date)

@main.route('/user/<uname>/blogs')
def user_blogs(uname):
    user = User.query.filter_by(username=uname).first()
    blogs = Blog.query.filter_by(user_id = user.id).all()
    blogs_count = Blog.count_blogs(uname)
    user_joined = user.date_joined.strftime('%b %d, %Y')

    return render_template("profile/blogs.html", user=user,blogs=blogs,blogs_count=blogs_count,date = user_joined)

@main.route('/subscribe',methods = ['POST','GET'])
def subscribe():
    email = request.form.get('subscriber')
    new_subscriber = Subscriber(email = email)
    new_subscriber.save_subscriber()
    mail_message("Subscribed to Zen Blog","email/welcome_subscriber",new_subscriber.email,new_subscriber=new_subscriber)
    flash('Successfuly subscribed')
    return redirect(url_for('main.index'))

@main.route('/blog/<blog_id>/delete', methods = ['POST'])
@login_required
def delete_post(blog_id):
    blog = Blog.query.get(blog_id)
    if blog.user != current_user:
        abort(403)
    blog.delete()
    flash("You have deleted your post successfully!")
    return redirect(url_for('main.index'))