from django.contrib.auth.models import User
from .models import Post
from rest_framework import status
from rest_framework.test import APITestCase


class PostListViewTests(APITestCase):
    def setUp(self):
        User.objects.create_user(username='rob', password='password')

    def test_can_list_posts(self):
        rob = User.objects.get(username='rob')
        Post.objects.create(owner=rob, title='test title')
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logged_in_user_can_create_post(self):
        self.client.login(username='rob', password='password')
        response = self.client.post('/posts/', {'title': 'test title'})
        count = Post.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_not_logged_in_cant_create_post(self):
        response = self.client.post('/posts/', {'title': 'test title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PostDetailViewTests(APITestCase):
    def setUp(self):
        rob = User.objects.create_user(username='rob', password='password')
        bertie = User.objects.create_user(username='bertie', password='bertpass')
        Post.objects.create(
            owner=rob,
            title='rob test title',
            content='rob test content'
        )
        Post.objects.create(
            owner=bertie,
            title='bertie tests title',
            content='bertie test content'
        )

    def test_can_retrieve_post_using_valid_id(self):
        response = self.client.get('/posts/1/')
        self.assertEqual(response.data['title'], 'rob test title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cant_retrieve_post_using_invalid_id(self):
        response = self.client.get('/posts/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_own_post(self):
        self.client.login(username='rob', password='password')
        response= self.client.put('/posts/1/', {'title': 'updated title'})
        post = Post.objects.filter(pk=1).first()
        self.assertEqual(post.title, 'updated title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cant_update_post_belonging_to_other_user(self):
        self.client.login(username='rob', password='password')
        response= self.client.put('/posts/2/', {'title': 'updated title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)