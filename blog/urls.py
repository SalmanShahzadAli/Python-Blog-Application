from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.post_list_view, name='post_list'),
    path('create/', views.create_post_view, name='create_post'),
    path('<int:pk>/', views.post_detail_view, name='post_detail'),
]