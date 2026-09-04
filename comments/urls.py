from django.urls import path
from . import views

app_name = 'comments'

urlpatterns = [
    path('add/<int:post_pk>/', views.add_comment_view, name='add_comment'),
]