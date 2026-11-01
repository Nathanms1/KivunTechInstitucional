from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from website.sitemaps import StaticViewSitemap

sitemaps = {
    'static': StaticViewSitemap,
}

urlpatterns = [
    path('', include('website.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
]

handler404 = 'website.views.handler404'
handler500 = 'website.views.handler500'
