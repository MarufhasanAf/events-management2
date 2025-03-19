from django.urls import path
from events.views import test,home,categories,participants,dashboard,event_details
urlpatterns = [

    path('test/', test ),
    path('', home, name="home"),
    path('dashboard', dashboard, name="dashboard"),
    path('category/', categories, name="category-list"),
    path('participants/', participants, name="participants-list"),
    path('event-details/', event_details, name="event-details")
]
