from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from .forms import ArticleForm, CommentForm
from .models import Article


def articles(request):
    keyword = request.GET.get("keyword")
    articles = Article.objects.all()

    if keyword:
        articles = articles.filter(title__icontains=keyword.strip())

    articles = articles.order_by("-created_date")
    return render(request, "articles.html", {"articles": articles, "keyword": keyword})


def index(request):
    return render(request, "index.html", {"numbers": [1, 2, 3, 4, 5, 6]})


def about(request):
    return render(request, "about.html")


@login_required(login_url="user:login")
def dashboard(request):
    articles = Article.objects.filter(author=request.user).order_by("-created_date")
    return render(request, "dashboard.html", {"articles": articles})


@login_required(login_url="user:login")
def add_article(request):
    form = ArticleForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        article = form.save(commit=False)
        article.author = request.user
        article.save()
        messages.success(request, "Makale başarıyla oluşturuldu.")
        return redirect("article:dashboard")

    return render(request, "addarticle.html", {"form": form})


def detail(request, id):
    article = get_object_or_404(Article, id=id)
    comments = article.comments.all()
    comment_form = CommentForm()
    return render(
        request,
        "detail.html",
        {"article": article, "comments": comments, "comment_form": comment_form},
    )


@login_required(login_url="user:login")
def update_article(request, id):
    article = get_object_or_404(Article, id=id, author=request.user)

    form = ArticleForm(request.POST or None, request.FILES or None, instance=article)

    if form.is_valid():
        form.save()
        messages.success(request, "Makale başarıyla güncellendi.")
        return redirect("article:dashboard")

    return render(request, "update.html", {"form": form, "article": article})


@login_required(login_url="user:login")
@require_POST
def delete_article(request, id):
    article = get_object_or_404(Article, id=id, author=request.user)
    article.delete()
    messages.success(request, "Makale başarıyla silindi.")
    return redirect("article:dashboard")


@require_POST
def add_comment(request, id):
    article = get_object_or_404(Article, id=id)
    form = CommentForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.article = article
        comment.save()
        messages.success(request, "Yorum başarıyla eklendi.")
    else:
        messages.error(request, "Yorum eklenemedi. Lütfen alanları kontrol edin.")

    return redirect(reverse("article:detail", kwargs={"id": id}))


# Backward-compatible aliases for older imports/tests.
addArticle = add_article
updateArticle = update_article
deleteArticle = delete_article
addComment = add_comment
