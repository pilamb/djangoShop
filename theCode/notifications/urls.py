from django.conf.urls import url

from .views import NotificationListView, NotificationDetailView

urlpatterns = [
    url(
        regex=r'^notification/(?P<pk>\d+)/$',
        view=NotificationDetailView.as_view(),
        name='notification_detail',
    ),
    url(
        regex=r'^notifications/(?P<pk>\d+)/$',
        view=NotificationListView.as_view(),
        name='notifications',
    ),
]

