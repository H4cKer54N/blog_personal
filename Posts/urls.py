from django.urls import path
from .views import *
from django.contrib.sitemaps import views

sitemaps = {
    'posts': PostSitemap,
}
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('tag/<str>', SearchByTag.as_view(), name='search_by_tag'),
    path('user/<str>', SearchByUser.as_view(), name='search_by_user'),
    path('detail/<slug>', DetailViewPost.as_view(), name='detail_post'),
    path('contact', ContactView.as_view(), name='contact'),
    path('sitemap.xml', views.sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

]