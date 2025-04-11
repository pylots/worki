from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search, name='search'),
    path('by_tag/<str:tag>/', views.pages_by_tag, name='pages_by_tag'),
    path('by_user/<str:user>/', views.pages_by_user, name='pages_by_user'),
    path('<str:slug>/', views.show_page, name='show_wiki_page'),
    path('<str:slug>/edit/', views.edit, name='edit_wiki_page'),
]
