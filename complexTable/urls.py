from django.urls import path

from . import views

app_name = 'complexTable'

# Patterns which leads to a page
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('complexTable', views.ComplexView.as_view(), name='complexTable'),
    path('detailedInfo', views.DetailedView.as_view(), name='detailedInfo'),
]

# Patterns which leads to download
downloadpatterns = [
    path('download', views.download, name='download'),
    path('downloadFiles', views.downloadFiles, name='downloadFiles'),
    path('downloadPOST', views.downloadPOST, name='downloadPOST'),
]

# Patterns to work with ajax
ajaxpatterns =[
    path('hist_post', views.hist_post, name='hist_post'),
    path('line2d_post', views.line2d_post, name='line2d_post'),
    path('heat2d_post', views.heat2d_post, name='heat2d_post'),
    path('distrib2d_post', views.distrib2d_post, name='distrib2d_post'),
    path('facet2d_post', views.facet2d_post, name='facet2d_post'),
]

# Concatenate all lists
urlpatterns += downloadpatterns
urlpatterns += ajaxpatterns