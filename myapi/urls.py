from rest_framework.routers import DefaultRouter
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'songs', views.SongViewSet)
router.register(r'follows', views.FollowViewSet)
router.register(r'reactions', views.ReactionViewSet)
router.register(r'comments', views.CommentViewSet)
router.register(r'savedposts', views.SavedPostViewSet)
router.register(r'notebooks', views.NotebookViewSet)
router.register(r'folders', views.FolderViewSet)
router.register(r'listitems', views.ListItemViewSet)
router.register(r'users', views.UserViewSet)

schema_view = get_schema_view(
   openapi.Info(
      title="LyricLib API",
      default_version='v1',
      description="API documentation for LyricLib",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@lyriclib.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Function-based views
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('', views.homePage, name='homepage'),

    # Class-based views for SongModel
    path('songs/create/', views.SongCreateView.as_view(), name='song_create'),
    path('songs/edit/<int:song_id>/', views.create_or_edit_song, name='song_edit'),

    # Class-based views for Artist
    path('artist/create/', views.ArtistCreateView.as_view(), name='artist_create'),
    path('artist/update/<int:pk>/', views.ArtistUpdateView.as_view(), name='artist_update'),

    # Class-based views for Composer
    path('composer/create/', views.ComposerCreateView.as_view(), name='composer_create'),
    path('composer/update/<int:pk>/', views.ComposerUpdateView.as_view(), name='composer_update'),

    # Class-based views for Lyricist
    path('lyricist/create/', views.LyricistCreateView.as_view(), name='lyricist_create'),
    path('lyricist/update/<int:pk>/', views.LyricistUpdateView.as_view(), name='lyricist_update'),

    # Class-based views for Tag
    path('tag/create/', views.TagCreateView.as_view(), name='tag_create'),
    path('tag/update/<int:pk>/', views.TagUpdateView.as_view(), name='tag_update'),

    # Class-based views for Language
    path('language/create/', views.LanguageCreateView.as_view(), name='language_create'),
    path('language/update/<int:pk>/', views.LanguageUpdateView.as_view(), name='language_update'),

    # Include the router URLs
    path('', include(router.urls)),

    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # At the very end of your urlpatterns list
    path('<path:request_path>', views.catch_all, name='catch_all'),

]
