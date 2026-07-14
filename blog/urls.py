from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.ArticleListView.as_view(), name='article_list'),
    path('category/<slug:slug>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/', views.ArticleDetailView.as_view(), name='article_detail'),
    path('category/', views.CategoryListView.as_view(), name='category_list'),  # <- новый путь
    path('category/<slug:slug>/', views.CategoryDetailView.as_view(), name='category_detail'),
]