from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from article import views as article_views

urlpatterns = [
    path("admin/", admin.site.urls),

    # Ana sayfalar
    path("", article_views.index, name="index"),
    path("about/", article_views.about, name="about"),

    # Makaleler
    path("articles/", include("article.urls")),

    # Kullanıcı işlemleri (login, register, dashboard)
    path("", include("user.urls")),
]

# Media dosyaları (DEV)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
