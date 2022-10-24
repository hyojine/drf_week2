from django.urls import path
from articles import views


urlpatterns = [
    path('', views.index, name='index'),
    path('<int:article_id>/', views.article_view, name='article_view'),
]