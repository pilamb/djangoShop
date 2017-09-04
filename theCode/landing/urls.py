from django.conf.urls import url

from .views import help_view, cookies_view, about_view, map_view, terms_view,\
    info_view


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
    url(
        regex=r'^terms/',
        view=terms_view,
        name='terms'
    ),
    url(
        regex=r'^info/',
        view=info_view,
        name='info'
    ),
]

