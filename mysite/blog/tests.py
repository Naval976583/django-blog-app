from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from taggit.models import Tag

from .models import Post, Comment

User = get_user_model()


# Test Data Setup (Reusable)
class PostTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="Admin",
            password="Admin@123"
        )
        self.post = Post.objects.create(
            title="Test Post",
            slug="test-post",
            body="This is a test post",
            author=self.user,
            status=Post.Status.PUBLISHED,
            publish=timezone.now()
        )

    # Test: Post List View
    def test_post_list_view(self):
        response = self.client.get(reverse('blog:post_list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Post")
        self.assertTemplateUsed(response, "blog/post/list.html")

    # Test: Post Detail View
    def test_post_detail_view(self):
        url = reverse(
            'blog:post_detail',
            args=[
                self.post.publish.year,
                self.post.publish.month,
                self.post.publish.day,
                self.post.slug
            ]
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.title)

    # Test: Comment Submission (POST)
    def test_post_comment(self):
        url = reverse("blog:post_comment", args=[self.post.id])

        response = self.client.post(url, {
            'name': 'Naval',
            'email': 'naval@test.com',
            'body': 'Nice post!'
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Comment.objects.count(), 1)

    # Test: Share Post View
    def test_post_share_view(self):
        url = reverse("blog:post_share", args=[self.post.id])

        response = self.client.post(url, {
            'name': 'Naval',
            'email': 'naval@test.com',
            'to': 'friend@test.com',
            'comments': 'Check this out'
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'sent')

    # Test: Search Functionality
    def test_post_search(self):
        response = self.client.get(
            reverse('blog:post_search'),
            {'query': 'Test'}
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Post")

    # Test: Tag Filtering
    def test_post_list_by_tag(self):
        tag = Tag.objects.create(name='Django', slug='django')
        self.post.tags.add(tag)

        response = self.client.get(
            reverse('blog:post_list_by_tag', args=[tag.slug])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.title)


