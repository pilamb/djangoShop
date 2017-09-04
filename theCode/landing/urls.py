from django.conf.urls import url

from .views import help_view, cookies_view, about_view, map_view


urlpatterns = [
    url(
        regex=r'^help/$',
        view=help_view,
        name='help',
    ),
    url(
        regex=r'^cookies/$',
        view=cookies_view,
        name='cookies',
    ),
    url(
        regex=r'^about/$',
        view=about_view,
        name='about',
    ),
    url(
        regex=r'^sitemap/$',
        view=map_view,
        name='map',
    ),
]

