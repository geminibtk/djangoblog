from django import forms

from .models import Article, Comment


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "content", "article_image"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["comment_author", "comment_content"]
        widgets = {
            "comment_content": forms.Textarea(attrs={"rows": 3}),
        }

    def clean_comment_author(self):
        author = self.cleaned_data["comment_author"].strip()
        if not author:
            raise forms.ValidationError("İsim alanı boş bırakılamaz.")
        return author

    def clean_comment_content(self):
        content = self.cleaned_data["comment_content"].strip()
        if not content:
            raise forms.ValidationError("Yorum alanı boş bırakılamaz.")
        return content
