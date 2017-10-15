from django.conf.urls import url

from .views import ProductDetailView, ProductsListView

urlpatterns = [
    url(
        regex=r'^detail/(?P<pk>\d+)/$',
        view=ProductDetailView.as_view(),
        name='detail',
    ),
    url(
        regex=r'^list/$',
        view=ProductsListView.as_view(),
        name='list',
    ),
]

