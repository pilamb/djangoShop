from django.conf.urls import url

from .views import EventListView

urlpatterns = [
    url(
        regex=r'^list/',
        view=EventListView.as_view(),
        name='events'
    )
]
