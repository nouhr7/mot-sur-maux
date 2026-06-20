from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from .models import Article, Author, Category


def article_list(request):
    """The blog index — every published article, newest first."""
    articles = Article.published.select_related("category", "author")

    featured = articles.filter(is_featured=True).first()
    queryset = articles.exclude(pk=featured.pk) if featured else articles

    paginator = Paginator(queryset, 9)
    page = paginator.get_page(request.GET.get("page"))

    return render(
        request,
        "blog/article_list.html",
        {
            "featured": featured,
            "page_obj": page,
            "categories": Category.objects.all(),
            "active_category": None,
        },
    )


def category_detail(request, slug):
    """All published articles within one theme."""
    category = get_object_or_404(Category, slug=slug)
    articles = Article.published.select_related("category", "author").filter(
        category=category
    )

    paginator = Paginator(articles, 9)
    page = paginator.get_page(request.GET.get("page"))

    return render(
        request,
        "blog/category.html",
        {
            "category": category,
            "page_obj": page,
            "categories": Category.objects.all(),
            "active_category": category,
        },
    )


def author_detail(request, slug):
    """An author's public page: their biography and their articles."""
    author = get_object_or_404(Author, slug=slug, is_active=True)
    articles = Article.published.select_related("category", "author").filter(
        author=author
    )

    paginator = Paginator(articles, 9)
    page = paginator.get_page(request.GET.get("page"))

    return render(
        request,
        "blog/author.html",
        {"author": author, "page_obj": page},
    )


def article_detail(request, slug):
    article = get_object_or_404(
        Article.published.select_related("category", "author"), slug=slug
    )
    related = (
        Article.published.filter(category=article.category)
        .exclude(pk=article.pk)[:3]
    )
    return render(
        request,
        "blog/article_detail.html",
        {"article": article, "related": related},
    )
