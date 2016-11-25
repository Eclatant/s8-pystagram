from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse
from django.db.utils import IntegrityError
from .models import Post
from .models import Category

class PostTest(TestCase):
    # def setUp(self):
    #     self.category = Category(name='...')
    #     category.save()

    def test_simple(self):
        self.assertEqual(1, 1)

    def test_save_post(self):
        category = Category(name='test category')
        category.save()

        post = Post()
        post.category = category
        post.content = 'hello world'
        self.assertIsNone(post.pk)
        post.save()
        self.assertIsNotNone(post.pk)

    def test_failed_to_save_post(self):
        post = Post()
        post.content = 'lorem issum'
        with self.assertRaises(IntegrityError):
            post.save()

        # category = Category(name='test category')
        # category.save()

        # post.category = category
        # post.save()

    def test_view_post(self):
        category = Category(name='test category')
        category.save()

        post = Post()
        post.category = category
        post.content = 'hello'
        post.save()

        url = reverse('photos:view', kwargs={'pk': post.pk})
        c = Client()
        res = c.get(url)
        self.assertEqual(res.status_code, 200)

