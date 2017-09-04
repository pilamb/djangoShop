from django.conf.urls import url


from .contact import page

urlpatterns = [
    url(
        regex=r'^',
        view=page,
        name='form',
    ),
]

