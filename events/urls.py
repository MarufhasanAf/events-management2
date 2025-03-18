from django.urls import path
from events.views import test
urlpatterns = [
    path('test/', test )
]
