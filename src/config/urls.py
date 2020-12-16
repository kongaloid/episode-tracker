from django.urls import path
from tracker.views import (
        SearchView,
        ShowListView,
        ShowAddView,
        ShowRemoveView
    )

urlpatterns = [
    path('', ShowListView.as_view(), name='home'),
    path('search/', SearchView.as_view(), name='search_str'),
    path('showadd/<pk>/', ShowAddView.as_view(), name='show_add'),
    path('showremove/<pk>/', ShowRemoveView.as_view(), name='show_remove'),
]