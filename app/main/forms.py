from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,SelectField
from wtforms.validators import Required

class BlogForm(FlaskForm):

    title = StringField('Blog Title',validators=[Required()])
    text = TextAreaField('Blog Description',validators=[Required()])
    category = SelectField('Type',choices=[('technology','Technology Blog'),('books','Books Blog'),('entertainment','Entertainment Blog')],validators=[Required()])
    submit = SubmitField('Submit')

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Bio.',validators = [Required()])
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    text = TextAreaField('Leave a comment:',validators=[Required()])
    submit = SubmitField('Submit')
