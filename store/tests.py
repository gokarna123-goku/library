from django.test import Client, TestCase
from django.urls import resolve, reverse

from store.views import add_blog

# Create your tests here.
class TestUrls(TestCase):
    def setUp(self):
      self.user = User.objects.create(username='testuser')
      self.user.set_password('12345')
      self.user.save()
      self.c = Client()
      self.c.login(username='testuser', password='12345')
      self.admin = Client()
      self.admin.login(username='admin', password='admin')


    def test_blog_create_url(self):
        url = reverse(add_blog)
        self.assertEquals(resolve(url).func,add_blog)

    def test_blog_update_url(self):
      self.assertEqual(
          reverse('blog_detail_view' ,kwargs={'slug': "random-slug"}),
          '/blog/random-slug/detail')
    
    def test_blog_delete_url(self):
      self.assertEqual(
          reverse('blog_delete_form' ,kwargs={'slug': "random-slug"}),
          '/blog/random-slug/delete')

    def test_blog_detail_url(self):
      self.assertEqual(
          reverse('blog_detail_view' ,kwargs={'slug': "random-slug"}),
          '/blog/random-slug/detail')
    
    def test_blog_view(self):
      c = Client()
      req = self.c.get("/blog/")
      self.assertEqual(req.status_code, 200)

    def test_add_product(self):
      response = self.c.post(reverse('add_product'),{
        "id": "12",
        "name": "test_product",
        "tag": "skincare",
        "price": "123",
        "description": "test_decription",
      })
      self.assertEqual(response.status_code, 302)