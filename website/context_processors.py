from django.templatetags.static import static


def seo_urls(request):
    return {
        'canonical_url': request.build_absolute_uri(request.path),
        'site_url': request.build_absolute_uri('/'),
        'og_image_url': request.build_absolute_uri(static('img/og-image.jpg')),
        'logo_url': request.build_absolute_uri(static('img/logo/kivun-horizontal-dark.png')),
    }
