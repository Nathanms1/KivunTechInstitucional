from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    changefreq = 'monthly'

    def items(self):
        return ['website:home', 'website:privacy_policy']

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        return 1.0 if item == 'website:home' else 0.3
