from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Article, Comment


class ArticleViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="author", password="StrongPass123!")
        self.article = Article.objects.create(
            author=self.user,
            title="Test makalesi",
            content="Test içerik",
        )

    def test_delete_article_requires_post(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("article:delete", args=[self.article.id]))

        self.assertEqual(response.status_code, 405)
        self.assertTrue(Article.objects.filter(id=self.article.id).exists())

    def test_delete_article_with_post_removes_article(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("article:delete", args=[self.article.id]))

        self.assertRedirects(response, reverse("article:dashboard"))
        self.assertFalse(Article.objects.filter(id=self.article.id).exists())

    def test_add_comment_strips_valid_input(self):
        response = self.client.post(
            reverse("article:comment", args=[self.article.id]),
            {
                "comment_author": "  Ziyaretçi  ",
                "comment_content": "  Güzel yazı.  ",
            },
        )

        self.assertRedirects(response, reverse("article:detail", args=[self.article.id]))
        comment = Comment.objects.get(article=self.article)
        self.assertEqual(comment.comment_author, "Ziyaretçi")
        self.assertEqual(comment.comment_content, "Güzel yazı.")

    def test_add_comment_rejects_blank_content(self):
        response = self.client.post(
            reverse("article:comment", args=[self.article.id]),
            {
                "comment_author": "Ziyaretçi",
                "comment_content": "   ",
            },
        )

        self.assertRedirects(response, reverse("article:detail", args=[self.article.id]))
        self.assertEqual(Comment.objects.count(), 0)
