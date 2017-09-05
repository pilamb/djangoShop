from django.conf.urls import url

from .views import UserModelListView, UserModelUpdateView, \
    UserModelDeleteView, UserModelDetailView


urlpatterns = [
    url(
        regex=r'^detailUser/(?P<pk>\d+)/$',
        view=UserModelDetailView.as_view(),
        name='user_detail',
    ),
    url(
        regex=r'^editUser/(?P<pk>\d+)/$',
        view=UserModelUpdateView.as_view(),
        name='user_edit',
    ),
    url(
        regex=r'^deleteUser/(?P<pk>\d+)/$',
        view=UserModelDeleteView.as_view(),
        name='user_delete',
    ),
    url(
        regex=r'^listUsers/',
        view=UserModelListView.as_view(),
        name='users_list',
    ),
]