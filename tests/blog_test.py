from app.models import Comment,User,Blog
from app import db
import unittest

class BlogModelTest(unittest.TestCase):
    def setUp(self):
        self.user_James = User(username = 'James',password = 'potato', email = 'james@ms.com')
        self.new_blog = Blog(id=1,blog_title='Test',blog_content='This is a test blog',category="technology",user = self.user_James)

    def tearDown(self):
        Pitch.query.delete()
        User.query.delete()

    def test_check_instance_variables(self):
        self.assertEquals(self.new_blog.blog_title,'Test')
        self.assertEquals(self.new_blog.blog_content,'This is a test blog')
        self.assertEquals(self.new_blog.category,"technology")
        self.assertEquals(self.new_blog.user,self.user_James)

    def test_save_blog(self):
        self.new_blog.save_blog()
        self.assertTrue(len(Blog.query.all())>0)

    def test_get_blog_by_id(self):
        self.new_blog.save_blog()
        got_blog = Blog.get_blog(1)
        self.assertTrue(got_blog is not None)