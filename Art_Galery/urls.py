"""Art_Galery URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin

from django.urls import path, include
from drf_yasg import openapi

from drf_yasg.views import get_schema_view
from rest_framework.routers import DefaultRouter

from Art_Galery import settings
from comment.views import CommentViewSet
from main.views import PostView, RatingViewSet

router = DefaultRouter()
router.register('posts', PostView)
router.register('comments', CommentViewSet)
router.register('rating', RatingViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description"
    ),

    public=True,
)

urlpatterns = [
    path('v1/api/docs/', schema_view.with_ui()),
    path('v1/api/', include(router.urls)),
    path('v1/api/account/', include('account.urls')),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
