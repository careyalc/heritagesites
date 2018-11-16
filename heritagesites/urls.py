from django.urls import path
from . import views 
from django_filters.views import FilterView

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('about/', views.AboutPageView.as_view(), name='about'),
    path('sites/', views.SiteListView.as_view(), name='sites'),
    path('sites/<int:pk>/', views.SiteDetailView.as_view(), name='site_detail'),
    path('countriesareas/', views.CountryAreaListView.as_view(), name='countriesareas'),
    path('countriesareas/<int:pk>/', views.CountryAreaDetailView.as_view(), name='countriesareas_detail'),
    path('sites/new/', views.SiteCreateView.as_view(), name='site_new'),
	path('sites/<int:pk>/delete/', views.SiteDeleteView.as_view(), name='site_delete'),
	path('sites/<int:pk>/update/', views.SiteUpdateView.as_view(), name='site_update'),
	path('site_filter', views.SiteFilterView.as_view(), name='site_filter') #had search instead before here and on base 
]